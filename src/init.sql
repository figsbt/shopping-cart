CREATE TABLE IF NOT EXISTS users ( \
    id SERIAL PRIMARY KEY, \
    email_id VARCHAR(255) NOT NULL, \
    pwd_hash VARCHAR(255) NOT NULL, \
    name VARCHAR(255) NOT NULL, \
    is_active BOOLEAN DEFAULT TRUE, \
    is_admin BOOLEAN DEFAULT FALSE, \
    UNIQUE(email_id) \
);

CREATE TABLE IF NOT EXISTS items ( \
    id SERIAL PRIMARY KEY, \
    item_name VARCHAR(255) NOT NULL, \
    item_details VARCHAR(255) NOT NULL, \
    stock INT NOT NULL, \
    cost FLOAT \
);

CREATE TABLE IF NOT EXISTS carts ( \
    id SERIAL PRIMARY KEY, \
    user_ref INT NOT NULL, \
    items_ref JSONB, \
    UNIQUE(user_ref) \
);