CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS trees (
    id TEXT PRIMARY KEY DEFAULT (
        SELECT substring(u::text, 1, 4) || '-' ||
               substring(u::text, 6, 4) || '-' ||
               substring(u::text, 11, 4) || '-' ||
               substring(u::text, 16, 4)
        FROM (SELECT uuid_generate_v4() AS u) t
    ),
    longitude DOUBLE PRECISION NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    height DOUBLE PRECISION NOT NULL
);
