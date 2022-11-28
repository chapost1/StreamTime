import UnprocessedVideo from './uploaded-video';
import Video from './video';

export interface UserVideosList {
    unprocessedVideos: UnprocessedVideo[];
    videos: Video[];
}