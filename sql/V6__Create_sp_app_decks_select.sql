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
                        app_decks.cards,
                        app_decks.groups
        FROM            app_decks
        JOIN            app_users
                        ON  app_decks.user_id = app_users.id AND
                            app_users.api_key = apiKey
        WHERE           app_decks.id = deckId
    )
    SELECT      row_to_json(d.*)
    FROM        d;

END;
$$

LANGUAGE plpgsql;
