CREATE TABLE IF NOT EXISTS clients (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    document VARCHAR(18) NOT NULL UNIQUE,
    phone VARCHAR(20),
    date_created TIMESTAMP NOT NULL,
    date_updated TIMESTAMP NOT NULL,
    deleted_at TIMESTAMP
);

INSERT INTO clients (id, name, email, document, phone, date_created, date_updated, deleted_at)
VALUES (
    '550e8400-e29b-41d4-a716-446655440000',
    'Cliente Teste Local',
    'local@mecanicadm.com',
    '79013046002',
    '48999999000',
    now(), now(), null
) ON CONFLICT DO NOTHING;