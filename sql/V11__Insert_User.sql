CREATE OR REPLACE FUNCTION insert_user(new_email VARCHAR(255), new_uname VARCHAR(255), new_encrypted_pword VARCHAR(255)) RETURNS TABLE (jdoc JSON) AS
$FUNC$
BEGIN
    RETURN QUERY
    WITH x AS
        (INSERT INTO users
            (email, username, encrypted_password)
        VALUES          
            (new_email, new_uname, new_encrypted_pword)
        RETURNING       
            users.id,
            users.email,
            users.is_admin)
    SELECT ROW_TO_JSON(x.*)
    FROM x;
END; 
$FUNC$ LANGUAGE plpgsql;