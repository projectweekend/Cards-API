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
                        app_decks.api_key,
                        app_decks.cards
        FROM            app_decks
        WHERE           app_decks.api_key = apiKey
    )
    SELECT      JSON_AGG(i.*)
    FROM        i;
END;
$$

LANGUAGE plpgsql;
