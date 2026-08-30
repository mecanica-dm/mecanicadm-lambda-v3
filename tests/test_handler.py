import json

from src import db_client, handler, jwt_service


def test_token_emitido_com_cpf_valido(monkeypatch):
    monkeypatch.setattr(
        db_client, "fetch_client_by_cpf",
        lambda cpf: {
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


def test_cpf_invalido_retorna_422():
    event = {"body": json.dumps({"cpf": "00000000000"})}
    resp = handler.handler(event, None)
    assert resp["statusCode"] == 422


def test_cliente_nao_encontrado_retorna_404(monkeypatch):
    monkeypatch.setattr(db_client, "fetch_client_by_cpf", lambda cpf: None)

    event = {"body": json.dumps({"cpf": "52998224725"})}
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
