CREATE TABLE IF NOT EXISTS "app_decks"
(
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER REFERENCES app_users(id),
    cards       JSONB,
    groups      JSONB
);
