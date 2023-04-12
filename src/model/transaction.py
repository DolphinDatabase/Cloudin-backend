from .database import db
import datetime


class Transaction(db.Model):
    __tablename__ = "transaction"
    id = db.Column("trn_id", db.Integer, primary_key=True)
    status = db.Column("trn_status", db.String(50), nullable=False)
    created = db.Column("trn_created", db.DateTime, default=datetime.datetime.now())
    config_id = db.Column("cfg_id", db.Integer, db.ForeignKey("config.cfg_id"))
    file = db.relationship("File", backref="transaction")

    def __repr__(self):
        return "<Transaction %r>" % self.id
