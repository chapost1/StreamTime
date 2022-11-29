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
                title: 'Crown the Empire - Millennia',
                description: `Hey there shadow.
                You didn't seem to care at all when you watched me go.
                I know young love is just a dream.
                We were only seventeen.
                But you're the only love I've known.
                
                So please just let me go if you're done.
                Cuz it's hope that kills this heart.
                So please set me free, kill the spark.
                I've been gone from this world for what seems like millennia.
                Looking for nothing short of a miracle.
                I only ever wanted to come home.
                Please won't you let me go?
                When I have nowhere left I can run away.
                Will you lie to me, tell me I'll be okay.
                Close my eyes and lay me in my tomb.
                Then pull the trigger and send me home.
                
                So how did I get so far from my yesterdays another broken heart now just a memory.
                I should've never.
                I should've left this awful town and never found out how to love.
                So I don't wanna know about the things that you regret now that we're dead and over and done.
                Get away from me and leave my heart under the rug.
                
                So please just let me go if you're done.
                Cuz it's hope that ills the heart.
                So please set me free, kill the spark.
                I've been gone from this world for what seems like millennia.
                Looking for nothing short of a miracle.
                I only ever wanted to come home.
                Please wont you let me go?
                When I have nowhere left I can run away.
                Will you lie to me, tell me I'll be okay.
                Close my eyes and lay me in my tomb.
                Then pull the trigger and send me...`,
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
