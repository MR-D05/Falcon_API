CREATE OR REPLACE FUNCTION fetch_name(user_id INTEGER) RETURNS TABLE (jdoc JSON) AS
$FUNC$
BEGIN
    RETURN QUERY
    WITH x AS
        (SELECT 
            users.username,
            users.is_admin
        FROM users
        WHERE 
            users.id = user_id)
    SELECT ROW_TO_JSON(x.*)
    FROM x;
END; 
$FUNC$ LANGUAGE plpgsql;