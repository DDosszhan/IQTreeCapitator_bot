-- enable pgcrypto (for gen_random_uuid)
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- function that generates id in format xxxx-xxxx-xxxx-xxxx
CREATE OR REPLACE FUNCTION generate_tree_id()
RETURNS TEXT
LANGUAGE plpgsql
AS $$
DECLARE
    u TEXT := replace(gen_random_uuid()::text, '-', ''); -- 32 hex chars, no dashes
BEGIN
    RETURN substring(u, 1, 4)
         || '-' || substring(u, 5, 4)
         || '-' || substring(u, 9, 4)
         || '-' || substring(u, 13, 4);
END;
$$;

-- create table
CREATE TABLE IF NOT EXISTS trees (
    id TEXT PRIMARY KEY DEFAULT generate_tree_id(),
    longitude DOUBLE PRECISION NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    height DOUBLE PRECISION NOT NULL,
    owner_username TEXT NOT NULL
);
