from flask import Blueprint, jsonify, make_response, request
from http.client import HTTPException
from ..schema.configSchema import ConfigSchema
from ..model.database import db
from ..model.config import Config

config_bp = Blueprint("config", __name__, url_prefix="/config")


@config_bp.route("/", methods=["GET"], strict_slashes=False)
def list_config():
    schema = ConfigSchema(many=True)
    query = Config().query.all()
    response = jsonify(schema.dump(query))
    return make_response(response, 200)


@config_bp.route("/", methods=["POST"], strict_slashes=False)
def create_config():
    body = request.get_json()
    data = Config(
        body["origin"],
        body["destiny"],
        body["originFolder"],
        body["destinyFolder"],
        body["originToken"],
        body["destinyToken"],
    )
    db.session.add(data)
    db.session.commit()
    schema = ConfigSchema()
    response = jsonify(schema.dump(data))
    return make_response(response, 200)
