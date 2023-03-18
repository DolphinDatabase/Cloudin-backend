from flask import Blueprint, request, jsonify
from ..model.database import db
from ..schema.transactionSchema import TransactionSchema
import importlib.util

from ..model.transaction import Transaction
from ..model.file import File

tbp = Blueprint('transaction', __name__, url_prefix="/transaction")

@tbp.route('/', methods=['GET'])
def list_transaction():
    schema = TransactionSchema(many=True)
    query = Transaction.query.all()
    transactions = schema.dump(query)
    return jsonify(transactions)

@tbp.route('/', methods=['POST'])
def create_transaction():
    body = request.get_json()
    origin_token = request.headers.get('origin_token')
    destiny_token = request.headers.get('destiny_token')
    transaction_data = {}

    #execute download
    origin = importlib.util.spec_from_file_location(body['origin'],"./src/blueprint/"+body['origin']+".py").loader.load_module()
    download = getattr(origin,body['origin']+"_download")
    for f in body['files']:
        metadata_download = download(f['file_id'],f['file_name'],origin_token)
        transaction_data[f['file_name']]['time'] += metadata_download['time']
        transaction_data[f['file_name']]['size'] += metadata_download['size']

    #execute upload
    destiny = importlib.util.spec_from_file_location(body['destiny'],"./src/blueprint/"+body['destiny']+".py").loader.load_module()
    upload = getattr(destiny,body['destiny']+"_upload")
    for f in body['files']:
        metadata_upload = upload(f['file_name'],destiny_token)
        transaction_data[f['file_name']]['time'] += metadata_upload['time']
    
    #save in db
    transaction = Transaction()
    transaction.origin = body['origin']
    transaction.destiny = body['destiny']
    transaction.status = "Em andamento"

    for f in transaction_data:
        file = File()
        file.name = f
        file.time = transaction_data[f]['time']
        file.size = transaction_data[f]['size']
        transaction.file.append(file)
        db.session.add(file)
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify(transaction_data)
        