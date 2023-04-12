from .database import db


class Config(db.Model):
    __tablename__ = "config"
    id = db.Column("cfg_id", db.Integer, primary_key=True)
    origin = db.Column("cfg_origin", db.String(50), nullable=False)
    destiny = db.Column("cfg_destiny", db.String(50), nullable=False)
    originFolder = db.Column("cfg_originFolder", db.String(50), nullable=False)
    destinyFolder = db.Column("cfg_destinyFolder", db.String(50), nullable=False)
    originToken = db.Column("cfg_originToken", db.String(255), nullable=False)
    destinyToken = db.Column("cfg_destinyToken", db.String(255), nullable=False)
    transaction = db.relationship("Transaction", backref="config")

    def __init__(self):
        None

    def __init__(
        self,
        origin=None,
        destiny=None,
        originFolder=None,
        destinyFolder=None,
        originToken=None,
        destinyToken=None,
    ):
        self.origin = origin
        self.destiny = destiny
        self.originFolder = originFolder
        self.destinyFolder = destinyFolder
        self.originToken = originToken
        self.destinyToken = destinyToken
