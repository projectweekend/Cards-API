CREATE FUNCTION sp_app_decks_select
(
    apiKey TEXT,
    deckId INTEGER
)

RETURNS TABLE
(
    jdoc JSON
) AS

$$
BEGIN
    RETURN      QUERY
    WITH d AS (
        SELECT          app_decks.id,
                        app_decks.api_key,
                        app_decks.cards
        FROM            app_decks
        WHERE           app_decks.api_key = apiKey AND
                        app_decks.id = deckId
    )
    SELECT      ROW_TO_JSON(d.*)
    FROM        d;

END;
$$

LANGUAGE plpgsql;
