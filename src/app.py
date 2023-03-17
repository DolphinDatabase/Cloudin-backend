from flask import Flask
#from .model.database import db 

from .blueprint.s3 import s3bp

app = Flask(__name__)
#pp.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://backend:api5sem@ec2-100-26-31-5.compute-1.amazonaws.com:3306/cloudin'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db.init_app(app)
#with app.app_context():
#    db.drop_all()
#    db.create_all()

app.register_blueprint(s3bp)

@app.route("/")
def helloWorld():
    return "Hello World!"
