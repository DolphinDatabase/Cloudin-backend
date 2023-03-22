from .database import db

import datetime

class Application(db.Model):
    __tablename__ = "application"
    app_id = db.Column("app_id",db.String(200),primary_key=True)
    created = db.Column("app_created",db.DateTime,default=datetime.datetime.now())
    transaction = db.relationship('Transaction', backref='application')
  
    def __repr__(self):
        return '<Application %r>' % self.id