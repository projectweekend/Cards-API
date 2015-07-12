CREATE TABLE IF NOT EXISTS "app_users"
(
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    api_key TEXT NOT NULL,
    UNIQUE (email),
    UNIQUE (api_key)
);
