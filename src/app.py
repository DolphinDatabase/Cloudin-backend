from flask import Flask, Response, jsonify
from .utils.MessageAnnouncer import MessageAnnouncer
from .model.database import db
from .schema.schema import ma
from .utils.scheduler import scheduler

from .model.config import Config
from .model.transaction import Transaction
from .model.file import File

from .schema.transactionSchema import TransactionSchema
from .services.google import GoogleService
from .services.s3 import s3Service
from flask_cors import CORS
from .blueprint.s3 import s3bp
from .blueprint.transaction import (
    tbp,
    new_transaction,
    update_transaction,
    make_transaction,
)
from .blueprint.google import drivebp, filesByFolderGoogle
from .blueprint.config import config_bp
from .responses.exceptions import config_error
import os
import json

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI" ] = "mysql://backend:api5sem@ec2-54-91-130-106.compute-1.amazonaws.com:3306/cloudin"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://dbuser:dbuser@localhost:3306/cloudin"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)
db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()

ma.init_app(app)
app.register_blueprint(s3bp)
app.register_blueprint(tbp)
app.register_blueprint(drivebp)
app.register_blueprint(config_bp)
config_error(app)

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


@scheduler.scheduled_job("interval", seconds=20)
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
                files = make_transaction(i,originService,destinyService)
                transaction = update_transaction(transaction, "Concluido", files)
                msg = format_sse(
                    data={"config": i.id, "transaction": schema.dump(transaction)},
                    event="updateTransaction",
                )
                announcer.announce(msg=msg)


@app.route("/")
def helloWorld():
    return "Hello World!"
