import Video from './video';
import { IVideosPage } from "../../backend/videos.types";
import assertField from '../assert-field';

class VideosPage {
    videos: Video[];
    next: string | null;
    

    constructor(videos: Video[], next: string | null) {
        assertField(this.constructor.name, 'videos', videos);
        this.videos = videos;
        this.next = next || null;
    }

    public hasNext(): boolean {
        const hasNext = Boolean(this.next && this.next !== null);
        const notAllVideosLoaded = 0 < this.videos.length;
        return hasNext && notAllVideosLoaded;
    }

    static fromInterface(source: IVideosPage): VideosPage {
        return new VideosPage(
            source.videos.map(Video.fromInterface),
            source.next || null
        )
    }

    public toInterface(): IVideosPage {
        return {
            next: this.next || null,
            videos: this.videos.map(v => v.toInterface()),
        }
    }
}

export default VideosPage;