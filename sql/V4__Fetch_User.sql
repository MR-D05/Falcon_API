CREATE OR REPLACE FUNCTION fetch_user(uname VARCHAR(255)) RETURNS TABLE (jdoc JSON) AS
$FUNC$
BEGIN
    RETURN QUERY
    WITH x AS
        (SELECT 
            users.id,
            users.email,
            users.encrypted_password,
            users.reset_password_token,
            users.username,
            users.is_admin
        FROM users
        WHERE 
            users.username = uname)
    SELECT ROW_TO_JSON(x.*)
    FROM x;
END; 
$FUNC$ LANGUAGE plpgsql;