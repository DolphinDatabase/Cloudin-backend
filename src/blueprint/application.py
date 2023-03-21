from flask import Blueprint, request, jsonify

#Carrego o SQLAlchemy
from ..model.database import db
#Carrego as colunas do insert
from ..schema.transactionSchemaSaveApplicationID import transactionSchemaSaveApplicationID
#Carrego o modelo da tabela
from ..model.application import Application


appl = Blueprint('application', __name__, url_prefix='/application')


@appl.route('/', methods=['GET'])
def list_application():
    schema = transactionSchemaSaveApplicationID(many=True)
    query = Application.query.all()
    applications = schema.dump(query)
    return jsonify(applications)

@appl.route('/', methods=['POST'])
def create_application():
    application_id = request.json.get('application_id')
    
    #save in db
    transaction = Application()
    transaction.application_id = application_id
    
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'mensagem': 'Operação concluída'})
