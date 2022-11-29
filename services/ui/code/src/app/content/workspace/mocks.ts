import { UserVideosList } from '../../core/models/entities/videos/types';
import UnprocessedVideo from '../../core/models/entities/videos/unprocessed-video';
import Video from '../../core/models/entities/videos/video';

export const userVideosList: UserVideosList = {
    unprocessedVideos: [
        UnprocessedVideo.fromInterface(
            {// still processing 
                hash_id: '69e14f7b-4b90-456a-9883-87be71e09bf5',
                user_id: 'ae6d14eb-d222-4967-98d9-60a7cc2d7891',
                upload_time: '2022-10-26T20:18:37.406479+00:00'
            }
        ),
        UnprocessedVideo.fromInterface(
            {// failed to process 
                hash_id: '19e14f7b-4b90-456a-9883-87be71e09bf2',
                user_id: 'ae6d14eb-d222-4967-98d9-60a7cc2d7891',
                upload_time: '2022-11-28T20:18:30.406479+00:00',
                failure_reason: 'Corrupted/Invalid file'
            }
        )
    ],
    videos: [
        Video.fromInterface(
            {// unlisted
                hash_id: '29rf4f7b-4b90-456a-9883-87be71e09bf5',
                user_id: 'ae6d14eb-d222-4967-98d9-60a7cc2d7891',
                upload_time: '2022-11-28T20:18:37.406479+00:00',
                size_in_bytes: 1.6e+6,
                duration_seconds: 600,
                thumbnail_url: 'https://i.ytimg.com/vi/b7DrwqoHAGA/hqdefault.jpg',
                video_type: 'video/mp4',
                is_private: false,
                listing_time: null
            },
        ),
        Video.fromInterface(
            {// listed
                hash_id: '29rf4f7b-4b90-456a-9883-87be71e09bf5',
                user_id: 'ae6d14eb-d222-4967-98d9-60a7cc2d7891',
                upload_time: '2022-11-28T20:18:37.406479+00:00',
                size_in_bytes: 123,
                duration_seconds: 500,
                thumbnail_url: 'https://i.ytimg.com/vi/xZ2yP7iUDeg/hq720.jpg',
                video_type: 'video/mp4',
                is_private: true,
                listing_time: '2022-11-28T20:18:41.406479+00:00'
            }
        ),
    ]
}
