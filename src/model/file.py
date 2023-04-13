from utils.database import db
from sqlalchemy.dialects.mysql import TIME


class File(db.Model):
    __tablename__ = "file"
    id = db.Column("fil_id", db.Integer, primary_key=True)
    name = db.Column("fil_name", db.String(100))
    size = db.Column("fil_size", db.Float)
    time = db.Column("fil_time", TIME())
    transaction_id = db.Column(
        "trn_id", db.Integer, db.ForeignKey("transaction.trn_id")
    )

    def __repr__(self):
        return "<File %r>" % self.name
