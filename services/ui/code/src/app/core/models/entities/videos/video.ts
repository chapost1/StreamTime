import { IVideo } from "../../backend/videos.types";
import assertField from "../assert-field";
import UploadedVideo from "./uploaded-video";
import { removeUndefinedValuesKeysFromObject } from '../../../../common/utils';

class Video extends UploadedVideo {
    title: string | null;
    description: string | null;
    sizeInBytes: number;
    durationSeconds: number;
    videoType: string;
    thumbnailUrl: string;
    isPrivate: boolean;
    listingTime: string | null;
    paginationIndex: number;

    constructor(
        hashId: string,
        userId: string,
        uploadTime: string,
        title: string | undefined,
        description: string | undefined,
        sizeInBytes: number,
        durationSeconds: number,
        videoType: string,
        thumbnailUrl: string,
        isPrivate: boolean,
        listingTime: string | undefined,
        paginationIndex: number
    ) {
        super(hashId, userId, uploadTime);

        this.title = title || null;
        this.description = description || null;
        this.listingTime = listingTime || null;

        assertField(this.constructor.name, 'sizeInBytes', sizeInBytes);
        this.sizeInBytes = sizeInBytes;
        assertField(this.constructor.name, 'durationSeconds', durationSeconds);
        this.durationSeconds = durationSeconds;
        assertField(this.constructor.name, 'videoType', videoType);
        this.videoType = videoType;
        assertField(this.constructor.name, 'thumbnailUrl', thumbnailUrl);
        this.thumbnailUrl = thumbnailUrl;
        assertField(this.constructor.name, 'isPrivate', isPrivate);
        this.isPrivate = isPrivate;
        assertField(this.constructor.name, 'paginationIndex', paginationIndex);
        this.paginationIndex = paginationIndex;
    }

    public isListed(): boolean {
        return this.listingTime !== null;
    }

    static override fromInterface(source: IVideo): Video {
        return new Video(
            source.hash_id,
            source.user_id,
            source.upload_time,
            source.title,
            source.description,
            source.size_in_bytes,
            source.duration_seconds,
            source.video_type,
            source.thumbnail_url,
            source.is_private,
            source.listing_time || undefined,
            source.pagination_index
        )
    }

    public override toInterface(): IVideo {
        const result = {
            ...super.toInterface(),
            title: this.title || undefined,
            description: this.description || undefined,
            size_in_bytes: this.sizeInBytes,
            duration_seconds: this.durationSeconds,
            video_type: this.videoType,
            thumbnail_url: this.thumbnailUrl,
            is_private: this.isPrivate,
            listing_time: this.listingTime || undefined,
            pagination_index: this.paginationIndex
        }
        removeUndefinedValuesKeysFromObject(result);
        return result;
    }
}



export default Video;