CREATE TABLE IF NOT EXISTS "files"
(
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL,
    uuidname    VARCHAR(255) NOT NULL,
    filename    VARCHAR(255) NOT NULL,
    username    VARCHAR(255) NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATE NULL
);   
    