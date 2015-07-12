CREATE FUNCTION sp_app_users_insert
(
    userDoc JSON
)

RETURNS VOID

AS

$$
BEGIN
    INSERT INTO     app_users
                    (
                        email,
                        api_key
                    )
    VALUES          (
                        CAST(userDoc ->> 'email' AS TEXT),
                        CAST(userDoc ->> 'api_key' AS TEXT)
                    );
END;
$$

LANGUAGE plpgsql;
