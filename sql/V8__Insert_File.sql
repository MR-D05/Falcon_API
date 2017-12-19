CREATE OR REPLACE FUNCTION insert_file(id INTEGER, identifiername VARCHAR(255), fname VARCHAR(255), uname VARCHAR(255)) RETURNS TABLE (jdoc JSON) AS
$FUNC$
BEGIN
    RETURN QUERY
    WITH x AS
        (INSERT INTO files
            (user_id, uuidname, filename, username)
        VALUES 
            (id, identifiername, fname, uname) 
        RETURNING
            files.id,
            files.uuidname,
            files.filename,
            files.username)
    SELECT ROW_TO_JSON(x.*)
    FROM x;
END;
$FUNC$ LANGUAGE plpgsql;