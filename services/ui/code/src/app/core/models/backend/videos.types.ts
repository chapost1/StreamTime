export interface IUploadedVideo {
    hash_id: string;
    user_id: string;
    file_name: string;
    upload_time: string;
}

export interface IUnprocessedVideo extends IUploadedVideo {
    failure_reason?: string;
}

export interface IVideo extends IUploadedVideo {
    title?: string;
    description?: string;
    size_in_bytes: number;
    duration_seconds: number;
    video_type: string;
    thumbnail_url: string;
    is_private: boolean;
    listing_time?: string | null;
}

export interface IUserVideosList {
    unprocessed_videos: IUnprocessedVideo[];
    videos: IVideo[];
}

export interface IWatchVideoRecord {
    watchable_url: string;
    video: IVideo;
}

export interface IVideosPage {
    videos: IVideo[];
    next: string | null;
}
