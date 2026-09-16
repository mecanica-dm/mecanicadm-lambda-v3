import jwt

from src import jwt_service


def test_create_token_carrega_issuer_documento_e_role(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "test-secret")

    token = jwt_service.create_token({
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Cliente Teste",
        "email": "cliente@teste.com",
        "document": "52998224725",
    })

    payload = jwt.decode(token, "test-secret", algorithms=["HS256"])

    assert payload["iss"] == jwt_service.ISSUER == "mecanicadm_api"
    assert payload["sub"] == "52998224725"
    assert payload["role"] == "CLIENT"
    assert payload["exp"] > payload["iat"]


def test_create_token_sem_secret_lanca_erro(monkeypatch):
    monkeypatch.delenv("JWT_SECRET", raising=False)

    try:
        jwt_service.create_token({
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Cliente Teste",
            "document": "52998224725",
        })
        assert False, "Deveria lançar RuntimeError sem JWT_SECRET"
    except RuntimeError as error:
        assert "JWT_SECRET" in str(error)