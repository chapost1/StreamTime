DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id uuid NOT NULL UNIQUE,
    username varchar(16) NOT NULL UNIQUE,
    email varchar (50) NOT NULL UNIQUE,
    first_name varchar(32) NOT NULL,
    last_name varchar(32) NOT NULL,
    password varchar(32) NOT NULL,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS videos;

CREATE TABLE videos (
    -- video
    hash_id uuid NOT NULL,
    user_id uuid NOT NULL,
    title varchar(128) NOT NULL,
    description text,
    size_in_bytes int NOT NULL DEFAULT 0,
    duration_seconds int NOT NULL DEFAULT 0,
    thumbnail_url varchar(255) NOT NULL,
    upload_time timestamptz NOT NULL,
    FOREIGN_KEY (user_id) REFERENCES users (id),
    UNIQUE (user_id, hash_id)
);

CREATE INDEX idx_videos_user_id ON videos(user_id);

CREATE INDEX idx_videos_hash_id ON videos(hash_id);