from flask import Response

from ..utils import *
from ..model import *
from ..schema import *

from .google import filesByFolderGoogle
from .s3 import filesByFolderS3
from .transaction import new_transaction, update_transaction


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


    @scheduler.scheduled_job("interval", seconds=10)
    def my_function():
        with app.app_context():
            schema = TransactionSchema()
            query = Config().query.all()
            for i in query:
                if i.origin == "s3":
                    new_files = filesByFolderS3(i.originToken, i.originFolder)
                elif i.origin == "google":
                    new_files = filesByFolderGoogle(i.originToken, i.originFolder)
                if new_files > 0:
                    transaction = new_transaction(i)
                    msg = format_sse(
                        data=f'{"config": {i.id}, "transaction": {schema.dump(transaction)}}',
                        event="newTransaction",
                    )
                    announcer.announce(msg=msg)
                    # make the transfer
                    transaction = update_transaction(
                        transaction, "Erro", [{"name": "teste", "time": 20, "size": 20}]
                    )
                    msg = format_sse(
                        data=f'{"config": {i.id}, "transaction": {schema.dump(transaction)}}',
                        event="updateTransaction",
                    )
                    announcer.announce(msg=msg)

    @app.route("/")
    def hello_world():
        return "Hello World!"
