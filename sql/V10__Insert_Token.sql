CREATE OR REPLACE FUNCTION insert_token(id INTEGER, uname VARCHAR(255), new_token VARCHAR(255)) RETURNS TABLE (jdoc JSON) AS
$FUNC$
BEGIN
    RETURN QUERY
    WITH x AS
        (INSERT INTO tokens
            (user_id, username, token)
        VALUES 
            (id, uname, new_token)
        RETURNING 
            tokens.id,
            tokens.user_id,
            tokens.username,
            tokens.token)
    SELECT ROW_TO_JSON(x.*)
    FROM x;
END; 
$FUNC$ LANGUAGE plpgsql;