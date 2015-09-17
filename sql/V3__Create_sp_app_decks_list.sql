CREATE FUNCTION sp_app_deck_list
(
    apiKey      TEXT
)

RETURNS TABLE
(
    record_count INTEGER,
    jdoc JSON
) AS

$$
DECLARE     recordCount INTEGER;

BEGIN
    SELECT      COUNT(*) INTO recordCount
    FROM        app_decks
    WHERE       app_decks.api_key = apiKey;

    RETURN      QUERY

    WITH result AS (
        SELECT          app_decks.id,
                        app_decks.api_key,
                        app_decks.deck
        FROM            app_decks
        WHERE           app_decks.api_key = apiKey
        ORDER BY        app_decks.id
    )

    SELECT      recordCount,
                JSON_AGG(result.*)
    FROM        result;
END;
$$

LANGUAGE plpgsql;
