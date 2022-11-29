import UnprocessedVideo from './unprocessed-video';
import Video from './video';

export interface UserVideosList {
    unprocessedVideos: UnprocessedVideo[];
    videos: Video[];
}