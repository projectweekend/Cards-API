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
        SET             cards = CAST(deckDoc ->> 'cards' AS JSONB),
                        groups = CAST(deckDoc ->> 'groups' AS JSONB)
        FROM            app_users
        WHERE           app_decks.id = deckId AND
                        app_decks.user_id = app_users.id AND
                        app_users.api_key = apiKey
        RETURNING       app_decks.id,
                        app_decks.cards,
                        app_decks.groups
    )
    SELECT      ROW_TO_JSON(i.*)
    FROM        i;
END;
$$

LANGUAGE plpgsql;
