CREATE TABLE IF NOT EXISTS "tokens"
(
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER REFERENCES users(id) NOT NULL,
    token       VARCHAR(255) NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATE NULL
);   
    
    
    
    