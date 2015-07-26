CREATE FUNCTION sp_app_decks_list
(
    apiKey TEXT
)

RETURNS TABLE
(
    resultDoc JSON
) AS

$$
BEGIN
    RETURN      QUERY
    WITH i as (
        SELECT          app_decks.id,
                        app_decks.cards,
                        app_decks.groups
        FROM            app_decks
        JOIN            app_users
                        ON  app_decks.user_id = app_users.id AND
                            app_users.api_key = apiKey
    )
    SELECT      JSON_AGG(i.*)
    FROM        i;
END;
$$

LANGUAGE plpgsql;
