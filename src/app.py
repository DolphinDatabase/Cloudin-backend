from flask import Flask
from flask_cors import CORS
import warnings
import os
from .utils import *
from .controller import *
from .exception.exceptions import configure_errors_handlers


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://backend:api5sem@ec2-54-91-130-106.compute-1.amazonaws.com:3306/cloudin'
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "SQLALCHEMY_DATABASE_URI", "sqlite:///:memory:"
)

# app.config["SQLALCHEMY_DATABASE_URI" ] = "mysql://backend:api5sem@ec2-54-91-130-106.compute-1.amazonaws.com:3306/cloudin"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)
warnings.filterwarnings("ignore", category=DeprecationWarning, module='flask_marshmallow')

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
configure_errors_handlers(app)
