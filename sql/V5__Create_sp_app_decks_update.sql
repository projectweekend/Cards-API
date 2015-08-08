CREATE FUNCTION sp_app_decks_update
(
    apiKey      TEXT,
    deckId      INTEGER,
    deckDoc     JSON
)

RETURNS TABLE
(
    jdoc JSON
) AS

$$
BEGIN
    RETURN     QUERY
    WITH i AS (
        UPDATE          app_decks
        SET             cards = CAST(deckDoc ->> 'cards' AS JSONB)
        WHERE           app_decks.api_key = apiKey AND
                        app_decks.id = deckId
        RETURNING       app_decks.id,
                        app_decks.api_key,
                        app_decks.cards
    )
    SELECT      ROW_TO_JSON(i.*)
    FROM        i;
END;
$$

LANGUAGE plpgsql;
