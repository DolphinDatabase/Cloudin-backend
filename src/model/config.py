from .database import db

class Config(db.Model):
    __tablename__ = "config"
    id = db.Column("cfg_id", db.Integer, primary_key=True)
    origin = db.Column("trn_origin", db.String(50), nullable=False)
    destiny = db.Column("trn_destiny", db.String(50), nullable=False)
    originFolder = db.Column("trn_originFolder", db.String(50), nullable=False)
    destinyFolder = db.Column("trn_destinyFolder", db.String(50), nullable=False)
    originToken = db.Column("trn_originToken", db.String(50), nullable=False)
    destinyToken = db.Column("trn_destinyToken", db.String(50), nullable=False)
    transaction = db.relationship("Transaction", backref="config_id")