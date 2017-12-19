CREATE OR REPLACE FUNCTION fetch_files(uname VARCHAR(255)) RETURNS TABLE (jdoc JSON) AS
$FUNC$
BEGIN
    RETURN QUERY
    WITH x AS
        (SELECT
            files.id,
            files.user_id,
            files.uuidname,
            files.filename,
            files.username
        FROM files
        WHERE       
            files.username = uname)
    SELECT ROW_TO_JSON(x.*)
    FROM x;
END; 
$FUNC$ LANGUAGE plpgsql;