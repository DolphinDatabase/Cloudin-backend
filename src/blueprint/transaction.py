from flask import Blueprint, request, jsonify
from ..model.database import db
from ..schema.transactionSchema import TransactionSchema
import importlib.util

from ..model.transaction import Transaction
from ..model.file import File

tbp = Blueprint('transaction', __name__, url_prefix="/transaction")

@tbp.route('/<id>', methods=['GET'])
def list_transaction(id):
    schema = TransactionSchema(many=True)
    query = Transaction.query.filter_by(application=id).all()
    transactions = schema.dump(query)
    return jsonify(transactions)

@tbp.route('/', methods=['POST'])
def create_transaction():
    body = request.get_json()
    origin_token = request.headers.get('origin_token')
    destiny_token = request.headers.get('destiny_token')
    application = request.headers.get('application')
    transaction_data = {}

    transaction = Transaction()
    transaction.origin = body['origin']
    transaction.destiny = body['destiny']
    transaction.status = "Em andamento"
    transaction.application = application
    
    db.session.add(transaction)
    db.session.commit()

    concluido = True
    #execute download
    origin = importlib.util.spec_from_file_location(body['origin'],"./src/blueprint/"+body['origin']+".py").loader.load_module()
    download = getattr(origin,"download_file")
    for f in body['files']:
        metadata_download = download(f['file_id'],f['file_name'],origin_token)
        if metadata_download.get('time'):
            transaction_data[f['file_name']]={'time':metadata_download['time'],'size':metadata_download['size']}
        else:
            print("webhook 1")
            concluido = False
            transaction_data = {f['file_name']:metadata_download}
            break

    #execute upload
    if concluido:
        destiny = importlib.util.spec_from_file_location(body['destiny'],"./src/blueprint/"+body['destiny']+".py").loader.load_module()
        upload = getattr(destiny,"upload_file")
        for f in body['files']:
            metadata_upload = upload(f['file_name'],destiny_token,body['origin'])
            if metadata_upload.get('time'):
                transaction_data[f['file_name']]['time']+= metadata_upload['time']
            else:
                print("webhook")
                concluido = False
                transaction_data = {f['file_name']:metadata_upload}
                break

    
    #save in db
    if concluido:
        transaction.status = "Concluido"
        for f in transaction_data:
            file = File()
            file.name = f
            file.time = transaction_data[f]['time']
            file.size = transaction_data[f]['size']
            transaction.file.append(file)
            db.session.add(file)
    else:
        transaction.status = "Erro"
    
    db.session.add(transaction)
    db.session.commit()
    return jsonify(transaction_data)


        