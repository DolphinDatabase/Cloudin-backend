from flask_marshmallow.fields import fields
from ..utils import ma


class FileSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)
    size = fields.String(dump_only=True)
    time = fields.String(dump_only=True)
