CREATE FUNCTION sp_app_deck_delete
(
    deckId      INTEGER,
    apiKey      TEXT
)

RETURNS BOOLEAN AS

$$
BEGIN
    DELETE FROM     app_decks
    WHERE           app_decks.id = deckId AND
                    app_decks.api_key = apiKey;
    RETURN          FOUND;
END;
$$

LANGUAGE plpgsql;
