from flask import Flask, Response
from .utils.MessageAnnouncer import MessageAnnouncer
from .model.database import db 
from .schema.schema import ma
from apscheduler.schedulers.background import BackgroundScheduler

from .model.config import Config
from .model.transaction import Transaction
from .model.file import File

from flask_cors import CORS
from .blueprint.s3 import s3bp
from .blueprint.transaction import tbp
from .blueprint.google import drivebp
from .blueprint.config import config_bp
from .responses.exceptions import config_error
import os

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI" ] = "mysql://backend:api5sem@ec2-54-91-130-106.compute-1.amazonaws.com:3306/cloudin"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://dbuser:dbuser@localhost:3306/cloudin"
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
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg


@app.route('/listen', methods=['GET'])
def listen():

    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return Response(stream(), mimetype='text/event-stream')

def myFunction():
    print("Automatic transfer")
    msg = format_sse(data='ok',event='message')
    announcer.announce(msg=msg)

sched = BackgroundScheduler(daemon=True)
sched.add_job(myFunction,'interval',seconds=10)
sched.start()

@app.route("/")
def helloWorld():
    return "Hello World!"
