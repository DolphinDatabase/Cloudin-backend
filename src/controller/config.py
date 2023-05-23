from flask import Blueprint, jsonify, make_response, request
from dotenv import set_key
from .default import configure_routes
from ..utils import *
from ..model import *
from ..schema import *
from ..services import *

config_blueprint = Blueprint("config", __name__, url_prefix="/config")

job = configure_routes


@config_blueprint.route("/", methods=["GET"], strict_slashes=False)
def list_config():
    services = {"google": GoogleService, "s3": s3Service}

    schema = ConfigSchema(many=True)
    configs = Config().query.all()

    for config in configs:
        config.originFolder = services[config.origin](
            config.originToken
        ).get_folder_name(config.originFolder)
        config.destinyFolder = services[config.destiny](
            config.destinyToken
        ).get_folder_name(config.destinyFolder)

    response = jsonify(schema.dump(configs))
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
