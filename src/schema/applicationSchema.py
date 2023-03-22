from .schema import ma
from flask_marshmallow.fields import fields
from .transactionSchema import TransactionSchema

class transactionSchemaSaveApplicationID(ma.Schema):
    app_id = fields.String(dump_only=True)
    created = fields.DateTime(dump_only=True)
    transaction = fields.Nested(TransactionSchema, many=True)