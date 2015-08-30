CREATE TABLE IF NOT EXISTS "app_decks"
(
    id          SERIAL PRIMARY KEY,
    api_key     TEXT,
    deck        JSONB
);
