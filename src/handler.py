import json
import logging
import os

from src import cpf_validator, db_client, jwt_service

logger = logging.getLogger()
logger.setLevel(logging.INFO)

CORS_ORIGIN = os.environ.get("CORS_ALLOWED_ORIGIN", "")


class InvalidRequestBody(ValueError):
    """Body da requisição não é um objeto JSON válido."""


def handler(event: dict, context) -> dict:
    try:
        body = _parse_body(event)
        raw_cpf = (body.get("cpf") or "").strip()

        if not raw_cpf:
            return _response(400, {"message": "CPF é obrigatório"})

        if not cpf_validator.is_valid(raw_cpf):
            return _response(422, {"message": "CPF inválido"})

        cpf_digits = cpf_validator.only_digits(raw_cpf)

        client = db_client.fetch_client_by_cpf(cpf_digits)
        if not client:
            return _response(404, {"message": "Cliente não encontrado"})

        token = jwt_service.create_token(client)
        logger.info("Token emitido para o CPF %s", cpf_validator.mask(cpf_digits))

        return _response(200, {
            "token": token,
            "token_type": "Bearer",
            "expires_in": jwt_service.get_expires_minutes() * 60,
        })

    except InvalidRequestBody:
        return _response(400, {"message": "Corpo da requisição em formato JSON inválido"})
    except Exception:
        logger.exception("Erro inesperado na Lambda")
        return _response(500, {"message": "Erro interno"})


def _parse_body(event: dict) -> dict:
    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError as error:
        raise InvalidRequestBody("body não é JSON válido") from error

    if not isinstance(body, dict):
        raise InvalidRequestBody("body deve ser um objeto JSON")

    return body


def _response(status_code: int, payload: dict) -> dict:
    headers = {"Content-Type": "application/json"}
    if CORS_ORIGIN:
        headers["Access-Control-Allow-Origin"] = CORS_ORIGIN

    return {
        "statusCode": status_code,
        "headers": headers,
        "body": json.dumps(payload, ensure_ascii=False),
    }
