from flask import Flask
from .utils import google_drive
from .model.database import db 
from .schema.schema import ma

from .model.transaction import Transaction
from .model.file import File

from .blueprint.s3 import s3bp
from .blueprint.transaction import tbp
from .blueprint.google import drivebp

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://backend:api5sem@ec2-54-227-6-234.compute-1.amazonaws.com:3306/cloudin'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dbuser:dbuser@localhost:3306/cloudin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()

ma.init_app(app)
app.register_blueprint(s3bp)
app.register_blueprint(tbp)
app.register_blueprint(drivebp)

@app.route("/")
def helloWorld():
    return "Hello World!"
