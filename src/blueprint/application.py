from flask import Blueprint, request, jsonify

#Carrego o SQLAlchemy
from ..model.database import db
#Carrego as colunas do insert
from ..schema.applicationSchema import transactionSchemaSaveApplicationID
#Carrego o modelo da tabela
from ..model.application import Application


appbp = Blueprint('application', __name__, url_prefix='/application')

@appbp.route('/', methods=['POST'])
def create_application():
    body = request.get_json()
    application = Application()
    application.app_id = body['app_id']
    db.session.add(application)
    db.session.commit()

    return {'msg':'Application created'}

