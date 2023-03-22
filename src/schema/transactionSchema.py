from .schema import ma
from flask_marshmallow.fields import fields
from .fileSchema import fileSchema

class TransactionSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    status = fields.String(dump_only=True)
    origin = fields.String(dump_only=True)
    destiny = fields.String(dump_only=True)
    created = fields.DateTime(dump_only=True)
    file = fields.Nested(fileSchema,many=True)