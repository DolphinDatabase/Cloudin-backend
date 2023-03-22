from .schema import ma
from flask_marshmallow.fields import fields

class fileSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)
    size = fields.String(dump_only=True)