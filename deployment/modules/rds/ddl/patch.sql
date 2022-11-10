INSERT INTO users (id, username, email, first_name, last_name, password)
VALUES ('ae6d14eb-d222-4967-98d9-60a7cc2d7891', 'dummy', 'foo@bar.com', 'foo', 'bar', 'secret');

INSERT INTO videos(hash_id, user_id, title, description, size_in_bytes, duration_seconds, video_type, thumbnail_url, upload_time, is_private, is_listed)
VALUES('ae6d14eb-d222-4967-98d9-60a7cc2d7891', 'ae6d14eb-d222-4967-98d9-60a7cc2d7891', 'Draft', 'some de', 0, 0, 'mp4', 'http://image.com', '2022-11-10T16:44:40.050259+00:00', false, false)
