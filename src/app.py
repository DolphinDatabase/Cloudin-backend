from flask import Flask
from flask_cors import CORS

from .utils import *
from .controller import *

from .exception.exceptions import config_error

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI" ] = "mysql://backend:api5sem@ec2-54-91-130-106.compute-1.amazonaws.com:3306/cloudin"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:toor@172.17.0.2:3306/cloudin"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)

db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()

ma.init_app(app)

app.register_blueprint(s3_blueprint)
app.register_blueprint(tbp)
app.register_blueprint(drivebp)
app.register_blueprint(config_blueprint)

configure_routes(app)
config_error(app)
