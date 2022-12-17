import Video from './video';
import { IWatchVideoRecord } from "../../backend/videos.types";
import assertField from '../assert-field';

class WatchVideoRecord {
    watchableUrl: string;
    video: Video;

    constructor(watchableUrl: string, video: Video) {
        assertField(this.constructor.name, 'watchableUrl', watchableUrl);
        this.watchableUrl = watchableUrl;
        assertField(this.constructor.name, 'video', video);
        this.video = video;
    }

    static fromInterface(source: IWatchVideoRecord): WatchVideoRecord {
        return new WatchVideoRecord(
            source.watchable_url,
            Video.fromInterface(source.video)
        )
    }

    public toInterface(): IWatchVideoRecord {
        return {
            watchable_url: this.watchableUrl,
            video: this.video.toInterface()
        }
    }
}

export default WatchVideoRecord;