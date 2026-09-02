import os

import psycopg2
from psycopg2.extras import RealDictCursor

_conn = None


def fetch_client_by_document(document_digits: str) -> dict | None:
    try:
        with _get_connection().cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT id, name, document FROM clients "
                "WHERE document = %s AND deleted_at IS NULL",
                (document_digits,),
            )
            row = cursor.fetchone()
            return dict(row) if row else None
    except psycopg2.OperationalError:
        _discard_connection()
        raise


def _get_connection():
    global _conn
    if _conn is not None and not _conn.closed:
        return _conn

    _conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        sslmode=os.environ.get("DB_SSLMODE", "require"),
        connect_timeout=5,
    )
    _conn.autocommit = True
    return _conn


def _discard_connection():
    global _conn
    if _conn is not None and not _conn.closed:
        _conn.close()
    _conn = None
