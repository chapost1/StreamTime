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

DROP TABLE IF EXISTS unprocessed_videos;

CREATE TABLE unprocessed_videos (
    hash_id uuid NOT NULL,
    user_id uuid NOT NULL,
    upload_time timestamptz NOT NULL,
    failure_reason varchar(64),
    CONSTRAINT fk_user_video_user_id FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (user_id, hash_id)
);

CREATE INDEX idx_unprocessed_videos_user_id ON unprocessed_videos(user_id);

DROP TABLE IF EXISTS videos;

CREATE TABLE videos (
    hash_id uuid NOT NULL,
    user_id uuid NOT NULL,
    title varchar(128) NOT NULL DEFAULT 'Draft',
    description text,
    size_in_bytes int NOT NULL DEFAULT 0,
    duration_seconds int NOT NULL DEFAULT 0,
    video_type varchar(32) NOT NULL,
    thumbnail_url varchar(255) NOT NULL,
    upload_time timestamptz NOT NULL,
    is_private boolean NOT NULL DEFAULT false,
    is_listed boolean NOT NULL DEFAULT false,
    CONSTRAINT fk_user_video_user_id FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (user_id, hash_id)
);

CREATE INDEX idx_videos_user_id ON videos(user_id);

CREATE INDEX idx_videos_hash_id ON videos(hash_id);