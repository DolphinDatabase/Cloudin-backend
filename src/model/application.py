from .database import db

import datetime

class Application(db.Model):
    __tablename__ = "application"
    id = db.Column("app_id",db.Integer, primary_key=True)
    application_id = db.Column("app_application_id",db.String(200))
    dt_log = db.Column("app_dt_log",db.DateTime,default=datetime.datetime.now())
  
    def __repr__(self):
        return '<Application %r>' % self.id