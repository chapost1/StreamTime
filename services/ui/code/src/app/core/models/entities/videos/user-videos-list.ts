import UploadedVideo from "./uploaded-video";
import UnprocessedVideo from './unprocessed-video';
import Video from './video';
import { IUserVideosList } from "../../backend/videos.types";

class UserVideosList {
    unprocessedVideos: UnprocessedVideo[];
    videos: Video[];

    constructor(unprocessedVideos: UnprocessedVideo[] = [], videos: Video[] = []) {
        this.unprocessedVideos = unprocessedVideos || [];
        this.videos = videos || [];
    }

    static fromInterface(source: IUserVideosList): UserVideosList {
        return new UserVideosList(
            source.unprocessed_videos.map(uv => UnprocessedVideo.fromInterface(uv)),
            source.videos.map(vid => Video.fromInterface(vid))
        )
    }

    public toInterface(): IUserVideosList {
        return {
            unprocessed_videos: this.unprocessedVideos.map(uv => uv.toInterface()),
            videos: this.videos.map(v => v.toInterface())
        }
    }

    public removeVideo(video: UploadedVideo): void {
        const list: UploadedVideo[] = this.getListByVideoType(video);
        this.removeVideoFromList(list, video.hashId);
    }

    private getListByVideoType(video: UploadedVideo): UploadedVideo[] {
        if (video instanceof UnprocessedVideo) {
            return this.unprocessedVideos;
        } else if (video instanceof Video) {
            return this.videos;
        }
        return [];
    }

    private removeVideoFromList(list: UploadedVideo[], hashId: string): void {
        const idx = list.findIndex(video => video.hashId === hashId);
        if (idx < 0) {
            return;
        }
        list.splice(idx, 1);
    }
}

export default UserVideosList;