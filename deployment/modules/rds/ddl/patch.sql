-- INSERT INTO users (id, username, email, first_name, last_name, password)
-- VALUES ('ae6d14eb-d222-4967-98d9-60a7cc2d7891', 'dummy', 'foo@bar.com', 'foo', 'bar', 'secret');

-- insert into unprocessed_videos (hash_id, user_id, file_name, upload_time, failure_reason) values ('19e14f7b-4b90-456a-9883-87be71e09bf2', 'ae6d14eb-d222-4967-98d9-60a7cc2d7891', 'bart.mp4', '2022-11-28T20:18:30.406479+00:00', 'Corrupted/Invalid file');

-- insert into videos (hash_id, user_id, file_name, upload_time, size_in_bytes, duration_seconds, thumbnail_url, video_type, is_private, listing_time, storage_thumbnail_key, storage_object_key) values ('0031d946-dae4-4e70-b09c-f1daaa0b464b', 'ae6d14eb-d222-4967-98d9-60a7cc2d7891', 'luffy.mp4', '2022-11-28T20:18:37.406479+00:00', 123, 500, 'https://i.ytimg.com/vi/b7DrwqoHAGA/hqdefault.jpg', 'video/mp4', false, null, 'booyaka_booyaka', 'another_key');