INSERT INTO users (id, username, email, first_name, last_name, password)
VALUES ('ae6d14eb-d222-4967-98d9-60a7cc2d7891', 'dummy', 'foo@bar.com', 'foo', 'bar', 'secret');

-- INSERT INTO unprocessed_videos(hash_id, user_id, upload_time, failure_reason)
-- VALUES('be6d14eb-d222-4967-98d9-60a7cc2d7891', 'ae6d14eb-d222-4967-98d9-60a7cc2d7891', '2022-11-10T16:44:40.050259+00:00', 'Corrupted video');


-- INSERT INTO videos(hash_id, user_id, title, description, size_in_bytes, duration_seconds, video_type, thumbnail_url, storage_object_key, upload_time, is_private, listing_time)
-- VALUES('ae6d14eb-d222-4967-98d9-60a7cc2d7891', 'ae6d14eb-d222-4967-98d9-60a7cc2d7891', 'Draft', 'Something short', 0, 0, 'mp4', 'http://image.com', 'vid_path.mp4', '2022-11-10T16:44:40.050259+00:00', false, '2022-11-10T16:50:40.050259+00:00');
