from flask_marshmallow.fields import fields
from ..utils import ma

from .file_schema import FileSchema


class TransactionSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    status = fields.String(dump_only=True)
    created = fields.DateTime()
    file = fields.Nested(FileSchema, many=True)
