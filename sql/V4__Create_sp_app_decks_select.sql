CREATE FUNCTION sp_app_deck_select
(
    deckId      INTEGER,
    apiKey      TEXT
)

RETURNS TABLE
(
    jdoc JSON
) AS

$$
BEGIN
    RETURN      QUERY
    WITH result AS (
        SELECT      app_decks.id,
                    app_decks.api_key,
                    app_decks.deck
        FROM        app_decks
        WHERE       app_decks.id = deckId AND
                    app_decks.api_key = apiKey
    )
    SELECT      ROW_TO_JSON(result.*)
    FROM        result;

END;
$$

LANGUAGE plpgsql;
