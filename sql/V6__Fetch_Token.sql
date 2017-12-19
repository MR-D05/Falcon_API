CREATE OR REPLACE FUNCTION fetch_token(tkn VARCHAR(255)) RETURNS TABLE (jdoc JSON) AS
$FUNC$
BEGIN
    RETURN QUERY
    WITH x AS
        (SELECT 
            tokens.user_id,
            tokens.username,
            tokens.token
        FROM tokens
        WHERE 
            tokens.token = tkn)
    SELECT ROW_TO_JSON(x.*)
    FROM x;
END; 
$FUNC$ LANGUAGE plpgsql;