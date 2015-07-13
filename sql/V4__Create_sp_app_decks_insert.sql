CREATE FUNCTION sp_app_deck_insert
(
    apiKey TEXT,
    deckDoc JSONB
)

RETURNS TABLE
(
    resultDoc JSON
) AS

$$
BEGIN
    RETURN      QUERY
    WITH i as (
        INSERT INTO     app_decks
                        (
                            user_id,
                            cards,
                            groups
                        )
        SELECT          app_users.id,
                        CAST(deckDoc ->> 'cards' AS JSONB),
                        CAST(deckDoc ->> 'groups' AS JSONB)
        FROM            app_users
        WHERE           app_users.api_key = apiKey
        RETURNING       app_decks.id,
                        app_decks.cards,
                        app_decks.groups
    )
    SELECT      ROW_TO_JSON(i.*)
    FROM        i;
END;
$$

LANGUAGE plpgsql;
