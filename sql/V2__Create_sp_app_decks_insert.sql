CREATE FUNCTION sp_app_deck_insert
(
    apiKey      TEXT,
    deckDoc     JSONB
)

RETURNS TABLE
(
    jdoc        JSON
) AS

$$
BEGIN
    RETURN      QUERY
    WITH inserted AS (
        INSERT INTO     app_decks
                        (
                            api_key,
                            deck
                        )
        VALUES          (
                            apiKey,
                            deckDoc
                        )
        RETURNING       app_decks.id,
                        app_decks.api_key,
                        app_decks.deck
    )
    SELECT      ROW_TO_JSON(inserted.*)
    FROM        inserted;
END;
$$

LANGUAGE plpgsql;
