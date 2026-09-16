import os
from datetime import datetime, timedelta, timezone

import jwt

DEFAULT_EXPIRES_MINUTES = 60

ISSUER = "mecanicadm_api"
CLIENT_ROLE = "CLIENT"


def get_expires_minutes() -> int:
    return int(os.environ.get("JWT_EXPIRES_MINUTES", DEFAULT_EXPIRES_MINUTES))


def create_token(client: dict) -> str:
    """Gera um JWT assinado com HS256 contendo os dados do cliente."""
    secret = os.environ.get("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET não configurado")

    now = datetime.now(timezone.utc)
    payload = {
        "iss": ISSUER,
        "sub": str(client.get("document", "")),
        "document": client.get("document", ""),
        "name": client.get("name", ""),
        "role": CLIENT_ROLE,
        "iat": now,
        "exp": now + timedelta(minutes=get_expires_minutes()),
    }

    return jwt.encode(payload, secret, algorithm="HS256")
