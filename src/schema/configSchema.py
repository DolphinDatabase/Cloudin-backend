from .schema import ma
from flask_marshmallow.fields import fields
from .transactionSchema import TransactionSchema


class ConfigSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    origin = fields.String(dump_only=True)
    destiny = fields.String(dump_only=True)
    originFolder = fields.String(dump_only=True)
    destinyFolder = fields.String(dump_only=True)
    originToken = fields.String(dump_only=True)
    destinyToken = fields.String(dump_only=True)
    transaction = fields.Nested(TransactionSchema, many=True)
