DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id uuid NOT NULL UNIQUE,
    username varchar(16) NOT NULL UNIQUE,
    email varchar (50) NOT NULL UNIQUE,
    first_name varchar(32) NOT NULL,
    last_name varchar(32) NOT NULL,
    password varchar(32) NOT NULL,
    PRIMARY KEY (id)
);

CREATE INDEX idx_users_user_id ON users(id);

DROP TABLE IF EXISTS unprocessed_videos CASCADE;

CREATE TABLE unprocessed_videos (
    hash_id uuid NOT NULL,
    user_id uuid NOT NULL,
    file_name varchar(255) NOT NULL,
    upload_time timestamptz NOT NULL,
    failure_reason varchar(64),
    CONSTRAINT fk_user_video_user_id FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (user_id, hash_id)
);

CREATE INDEX idx_unprocessed_videos_user_id ON unprocessed_videos(user_id);

DROP TABLE IF EXISTS videos CASCADE;

CREATE TABLE videos (
    hash_id uuid NOT NULL,
    user_id uuid NOT NULL,
    file_name varchar(255) NOT NULL,
    pagination_index serial,
    title varchar(128) NOT NULL DEFAULT 'Draft',
    description text,
    size_in_bytes int NOT NULL DEFAULT 0,
    duration_seconds int NOT NULL DEFAULT 0,
    video_type varchar(32) NOT NULL,
    thumbnail_url varchar(255) NOT NULL,
    storage_thumbnail_key varchar(255) NOT NULL,
    storage_object_key varchar(255) NOT NULL,
    upload_time timestamptz NOT NULL,
    is_private boolean NOT NULL DEFAULT false,
    listing_time timestamptz DEFAULT NULL,
    CONSTRAINT fk_user_video_user_id FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (user_id, hash_id)
);

CREATE INDEX idx_videos_user_id ON videos(user_id);

CREATE INDEX idx_videos_user_id_hash_id ON videos(user_id, hash_id);

CREATE INDEX idx_videos_pagination_index ON videos(pagination_index);

INSERT INTO users (id, username, email, first_name, last_name, password)
VALUES ('ae6d14eb-d222-4967-98d9-60a7cc2d7891', 'dummy', 'foo@bar.com', 'foo', 'bar', 'secret');
