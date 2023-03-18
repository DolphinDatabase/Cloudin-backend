from flask import Flask
from .model.database import db 
from .schema.schema import ma

from .model.transaction import Transaction
from .model.file import File

from .blueprint.s3 import s3bp
from .blueprint.transaction import tbp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://backend:api5sem@ec2-54-227-6-234.compute-1.amazonaws.com:3306/cloudin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from .utils import google_drive
from .model.database import db 

app = Flask(__name__)
app.secret_key = 'teste'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://backend:api5sem@ec2-100-26-31-5.compute-1.amazonaws.com:3306/cloudin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()

ma.init_app(app)
app.register_blueprint(s3bp)
app.register_blueprint(tbp)

@app.route("/")
def helloWorld():
    return "Hello World!"


@app.route('/auth/google')
def authenticate():
    return google_drive.authenticate()
    

@app.route('/auth/google/refresh-token')
def refresh_token():
    return google_drive.refresh_token()


@app.route('/google/files')
def list_files(access_token=''):
    return google_drive.list_files(access_token)


@app.route('/google/download')
def download_item(access_token='', file_id=''):
 
    return google_drive.download_file(access_token, file_id)


@app.route('/google/upload')
def upload_item():
 
    return google_drive.upload_file_to_drive()
