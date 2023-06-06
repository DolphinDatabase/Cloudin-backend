from flask import Response
from flask import make_response, request
from apscheduler.triggers.interval import IntervalTrigger

from ..utils import *
from ..model import *
from ..schema import *
from ..services import *
import os

from .google import filesByFolderGoogle
from .s3 import filesByFolderS3
from .transaction import new_transaction, update_transaction, make_transaction


def configure_routes(app):
    announcer = MessageAnnouncer()

    def format_sse(data: str, event=None) -> str:
        msg = f"data: {data}\n\n"
        if event is not None:
            msg = f"event: {event}\n{msg}"
        return msg

    @app.route("/listen", methods=["GET"])
    def listen():
        def stream():
            messages = announcer.listen()  # returns a queue.Queue
            while True:
                msg = messages.get()  # blocks until a new message arrives
                yield msg

        return Response(stream(), mimetype="text/event-stream")

    @scheduler.scheduled_job("interval", seconds=int(load_json_file()["JOB_TIME"]))
    @limit_bandwidth(int(getBandwidth() * (int(load_json_file()["BAND"]) / 100)))
    def myFunction():
        with app.app_context():
            schema = TransactionSchema()
            query = Config().query.all()
            for i in query:
                if i.origin == "google":
                    originService = GoogleService(i.originToken)
                elif i.origin == "s3":
                    originService = s3Service(i.originToken)
                if i.destiny == "google":
                    destinyService = GoogleService(i.destinyToken)
                elif i.destiny == "s3":
                    destinyService = s3Service(i.destinyToken)
                new_files = originService.files_by_folder(i.originFolder)
                if new_files > 0:
                    transaction = new_transaction(i)
                    msg = format_sse(
                        data={"config": i.id, "transaction": schema.dump(transaction)},
                        event="newTransaction",
                    )
                    announcer.announce(msg=msg)
                    try:
                        files = make_transaction(i, originService, destinyService)
                        if len(files) <= 0:
                            transaction = update_transaction(transaction, "Erro", [])
                        else:
                            transaction = update_transaction(
                                transaction, "Concluido", files
                            )
                    except Exception as e:
                        transaction = update_transaction(transaction, "Erro", [])

                    msg = format_sse(
                        data={"config": i.id, "transaction": schema.dump(transaction)},
                        event="updateTransaction",
                    )
                    announcer.announce(msg=msg)

    @app.route("/job", methods=["POST"], strict_slashes=False)
    def set_job_time():
        body = request.get_json()
        data = load_json_file()
        data["JOB_TIME"] = str(body["job"])
        data["BAND"] = str(body["band"])
        data["TRANSFER_TIME"] = str(body["transfer"])
        save_json_file(data)
        scheduler.remove_all_jobs()
        scheduler.add_job(myFunction, IntervalTrigger(seconds=int(body["job"])))
        return make_response({}, 200)

    @app.route("/job", methods=["GET"], strict_slashes=False)
    def get_job_time():
        data = load_json_file()
        return make_response(data, 200)

    @app.route("/")
    def helloWorld():
        return "Hello World!!!"

    return myFunction
