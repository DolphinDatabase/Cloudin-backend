from flask import Blueprint, jsonify, make_response, request

from utils.database import db
from model import *
from schema import *


config_blueprint = Blueprint("config", __name__, url_prefix="/config")

@config_blueprint.route("/", methods=["GET"], strict_slashes=False)
def list_config():
    schema = ConfigSchema(many=True)
    query = Config().query.all()
    response = jsonify(schema.dump(query))
    return make_response(response, 200)


@config_blueprint.route("/", methods=["POST"], strict_slashes=False)
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
