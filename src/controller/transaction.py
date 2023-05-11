from flask import Blueprint, request, jsonify, make_response
import importlib.util
import os

from ..model import *
from ..schema import *
from ..utils import *

from ..services.google import GoogleService
from ..services.s3 import s3Service

tbp = Blueprint("transaction", __name__, url_prefix="/transaction")


def new_transaction(config: Config):
    transaction = Transaction()
    transaction.status = "Em andamento"
    config.transaction.append(transaction)
    db.session.add(transaction)
    db.session.add(config)
    db.session.commit()
    return transaction


def update_transaction(transaction: Transaction, status, files):
    transaction.status = status
    for f in files:
        file = File()
        file.name = f["title"]
        file.time = f["time"]
        file.size = f["size"]
        transaction.file.append(file)
        db.session.add(file)
    db.session.add(transaction)
    db.session.commit()
    return transaction


def make_transaction(config: Config, originService, destinyService):
    transaction_data = []
    for f in originService.list_files_by_folder(config.originFolder):
        try:
            download = originService.download(f["id"], f["name"])
        except:
            for filename in os.listdir("./downloads/" + config.origin):
                file_path = os.path.join("./downloads/" + config.origin, filename)
                os.remove(file_path)
            return
        try:
            upload = destinyService.upload(
                f["name"], config.origin, config.destinyFolder
            )
            download["time"] += upload["time"]
            transaction_data.append(download)
            originService.remove_file(f["id"], f["name"], config.originFolder)
        except:
            for filename in os.listdir("./downloads/" + config.origin):
                file_path = os.path.join("./downloads/" + config.origin, filename)
                os.remove(file_path)
            return
    return transaction_data


@tbp.route("/<id>", methods=["GET"], strict_slashes=False)
def list_transaction(id):
    schema = TransactionSchema(many=True)
    query = Transaction.query.filter_by(application=id).all()
    transactions = schema.dump(query)
    response_body = jsonify(transactions)
    return make_response(response_body, 200)


@tbp.route("/", methods=["POST"], strict_slashes=False)
def create_transaction():
    body = request.get_json()
    origin_token = request.headers.get("origin_token")
    destiny_token = request.headers.get("destiny_token")
    application = request.headers.get("application")
    transaction_data = {}

    transaction = Transaction()
    transaction.origin = body["origin"]
    transaction.destiny = body["destiny"]
    transaction.status = "Em andamento"
    transaction.application = application

    db.session.add(transaction)
    db.session.commit()

    concluido = True
    # execute download
    origin = importlib.util.spec_from_file_location(
        body["origin"], "./src/controller/" + body["origin"] + ".py"
    ).loader.load_module()
    download = getattr(origin, "download_file")
    for f in body["files"]:
        metadata_download = download(f["file_id"], f["file_name"], origin_token)
        if metadata_download.get("time"):
            transaction_data[f["file_name"]] = {
                "time": metadata_download["time"],
                "size": metadata_download["size"],
            }
        else:
            message = f"Erro ao realizar o download do arquivo {f['file_name']}."
            return make_response(jsonify({"message": message}), 400)

    # execute upload
    if concluido:
        destiny = importlib.util.spec_from_file_location(
            body["destiny"], "./src/controller/" + body["destiny"] + ".py"
        ).loader.load_module()
        upload = getattr(destiny, "upload_file")
        for f in body["files"]:
            metadata_upload = upload(f["file_name"], destiny_token, body["origin"])
            if metadata_upload.get("time"):
                transaction_data[f["file_name"]]["time"] += metadata_upload["time"]
            else:
                message = f"Erro ao realizar o upload do arquivo {f['file_name']}."
                return make_response(jsonify({"message": message}), 400)

    # save in db
    if concluido:
        transaction.status = "Concluido"
        for f in transaction_data:
            file = File()
            file.name = f
            file.time = transaction_data[f]["time"]
            file.size = transaction_data[f]["size"]
            transaction.file.append(file)
            db.session.add(file)
    else:
        transaction.status = "Erro"

    db.session.add(transaction)
    db.session.commit()
    return make_response(jsonify(transaction_data))
