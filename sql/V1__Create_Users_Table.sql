CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE IF NOT EXISTS "users"
(
    id                              BIGSERIAL PRIMARY KEY,
    email                           VARCHAR(255) UNIQUE NOT NULL,
    encrypted_password              VARCHAR(255) NOT NULL,
    reset_password_token            UUID NOT NULL DEFAULT uuid_generate_v4(),
    reset_password_sent_at          DATE NULL,
    remember_created_at             DATE NULL,
    sign_in_count                   INTEGER NULL,
    current_sign_in_at              TIMESTAMP NULL,
    last_sign_in_at                 TIMESTAMP NULL,
    current_sign_in_ip              VARCHAR NULL,
    last_sign_in_ip                 VARCHAR NULL,
    created_at                      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at                      TIMESTAMP NULL,
    username                        VARCHAR(255) UNIQUE NULL,
    expires_at                      TIMESTAMP NULL,
    is_admin                        BOOLEAN DEFAULT FALSE,
    m2m_email_recipients_json       VARCHAR(255) NULL,
    mobile_can_read_all             BOOLEAN DEFAULT FALSE,
    m2m_sms_recipients_json         VARCHAR(255) NULL,
    can_use_hydrantenplan_app       BOOLEAN DEFAULT TRUE,
    can_add_sub_users               BOOLEAN DEFAULT FALSE,
    can_access_hydrants_global      BOOLEAN DEFAULT TRUE,
    can_access_gate_valves_global   BOOLEAN DEFAULT TRUE,
    super_user_id                   INTEGER DEFAULT NULL
);