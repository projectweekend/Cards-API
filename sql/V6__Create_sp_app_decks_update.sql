CREATE FUNCTION sp_app_deck_update
(
    deckId      INTEGER,
    apiKey      TEXT,
    deckDoc     JSONB
)

RETURNS TABLE
(
    jdoc    JSON
) AS

$$
BEGIN
    RETURN     QUERY
    WITH updated AS (
        UPDATE          app_decks
        SET             deck = deckDoc
        WHERE           app_decks.id = deckId AND
                        app_decks.api_key = apiKey
        RETURNING       app_decks.id,
                        app_decks.api_key,
                        app_decks.deck
    )
    SELECT      ROW_TO_JSON(updated.*)
    FROM        updated;
END;
$$

LANGUAGE plpgsql;
