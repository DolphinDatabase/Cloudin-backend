from flask import json


class StorageErrorException(Exception):
    code = 400
    description = "Erro de requisição para o storage"


class StorageAuthorizationException(Exception):
    code = 403
    descritption = "Erro de autorização ou autenticação"


def configure_errors_handlers(app):
    @app.errorhandler(StorageAuthorizationException)
    def handle_storage_authorization_exception(exception):
        response = exception.get_response()
        response.data = json.dumps(
            {
                "code": exception.code,
                "name": exception.name,
                "description": exception.description,
            }
        )

        response.content_type = "application/json"

        return response

    @app.errorhandler(StorageErrorException)
    def handle_storage_error_exception(exception):
        response = exception.get_response()
        response.data = json.dumps(
            {
                "code": exception.code,
                "name": exception.name,
                "description": exception.description,
            }
        )

        response.content_type = "application/json"

        return response
