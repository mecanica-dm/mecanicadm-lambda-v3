import base64
import json

from src import db_client, handler, jwt_service


def test_body_base64_encoded_retorna_400_sem_documento():
    body_b64 = base64.b64encode(json.dumps({"document": ""}).encode()).decode()
    event = {"body": body_b64, "isBase64Encoded": True}
    resp = handler.handler(event, None)
    assert resp["statusCode"] == 400
    assert "Documento" in json.loads(resp["body"])["message"]


def test_token_emitido_com_documento_valido(monkeypatch):
    monkeypatch.setattr(
        db_client, "fetch_client_by_document",
        lambda document: {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Cliente Teste",
            "document": "52998224725",
        },
    )

    monkeypatch.setattr(jwt_service, "create_token", lambda client: "token-fake")

    event = {"body": json.dumps({"document": "529.982.247-25"})}
    resp = handler.handler(event, None)

    assert resp["statusCode"] == 200
    assert json.loads(resp["body"])["token"] == "token-fake"


def test_token_emitido_com_cnpj_valido(monkeypatch):
    monkeypatch.setattr(
        db_client, "fetch_client_by_document",
        lambda document: {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Cliente PJ",
            "document": "12345678000195",
        },
    )

    monkeypatch.setattr(jwt_service, "create_token", lambda client: "token-fake")

    event = {"body": json.dumps({"document": "12.345.678/0001-95"})}
    resp = handler.handler(event, None)

    assert resp["statusCode"] == 200
    assert json.loads(resp["body"])["token"] == "token-fake"


def test_token_emitido_com_campo_cpf_compativel(monkeypatch):
    monkeypatch.setattr(
        db_client, "fetch_client_by_document",
        lambda document: {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Cliente Teste",
            "document": "52998224725",
        },
    )

    monkeypatch.setattr(jwt_service, "create_token", lambda client: "token-fake")

    event = {"body": json.dumps({"cpf": "52998224725"})}
    resp = handler.handler(event, None)

    assert resp["statusCode"] == 200
    assert json.loads(resp["body"])["token"] == "token-fake"


def test_documento_invalido_retorna_422():
    event = {"body": json.dumps({"document": "00000000000"})}
    resp = handler.handler(event, None)
    assert resp["statusCode"] == 422


def test_cnpj_invalido_retorna_422():
    event = {"body": json.dumps({"document": "12.345.678/0001-00"})}
    resp = handler.handler(event, None)
    assert resp["statusCode"] == 422


def test_cliente_nao_encontrado_retorna_404(monkeypatch):
    monkeypatch.setattr(db_client, "fetch_client_by_document", lambda document: None)

    event = {"body": json.dumps({"document": "52998224725"})}
    resp = handler.handler(event, None)
    assert resp["statusCode"] == 404


def test_body_invalido_retorna_400():
    event = {"body": "nao-e-json"}
    resp = handler.handler(event, None)
    assert resp["statusCode"] == 400


def test_body_json_nao_objeto_retorna_400():
    event = {"body": json.dumps([1, 2])}
    resp = handler.handler(event, None)
    assert resp["statusCode"] == 400
