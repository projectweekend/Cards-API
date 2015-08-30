CREATE FUNCTION sp_app_decks_insert
(
    apiKey      TEXT,
    deckDoc     JSONB
)

RETURNS TABLE
(
    resultDoc   JSON
) AS

$$
BEGIN
    RETURN      QUERY
    WITH i as (
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
    SELECT      ROW_TO_JSON(i.*)
    FROM        i;
END;
$$

LANGUAGE plpgsql;
