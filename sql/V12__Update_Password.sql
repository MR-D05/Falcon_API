CREATE OR REPLACE FUNCTION update_password(uname VARCHAR(255), new_password VARCHAR(255)) RETURNS BOOLEAN AS
$FUNC$
BEGIN
    UPDATE      users
    SET         encrypted_password = new_password
    WHERE       users.username = uname;
    RETURN      FOUND;
END; 
$FUNC$ LANGUAGE plpgsql;