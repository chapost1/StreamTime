import { IUploadedVideo } from "../../backend/videos.types";
import assertField from "../assert-field";

export interface IUserIdHashId {
    hashId: string;
    userId: string;
}

class UploadedVideo {
    hashId: string;
    userId: string;
    uploadTime: string;
    uploadTimeTS: number;

    sync: boolean;

    protected constructor(hashId: string, userId: string, uploadTime: string) {
        this.sync = false;

        assertField(this.constructor.name, 'hashId', hashId);
        this.hashId = hashId;
        assertField(this.constructor.name, 'userId', userId);
        this.userId = userId;
        assertField(this.constructor.name, 'uploadTime', uploadTime);
        this.uploadTime = uploadTime;
        this.uploadTimeTS = new Date(this.uploadTime).getTime();
    }

    static fromInterface(source: IUploadedVideo): UploadedVideo {
        return new UploadedVideo(
            source.hash_id,
            source.user_id,
            source.upload_time
        )
    }

    public toInterface(): IUploadedVideo {
        return {
            hash_id: this.hashId,
            user_id: this.userId,
            upload_time: this.uploadTime
        }
    }

    public clientSideId(): string {
        // base64 encoding adds padding to the end of the string, which is not allowed in URLs
        // it adds padding to make sure the decoded string is divisable by 3
        // the key contains 2 uuids, which are 36 bytes each, which is 72 bytes
        // that's already divisable by 3, therefore no padding is added
        // so to keep it as is, we don't add any separators and just concatenate the strings
        return btoa(`${this.hashId}${this.userId}`);
    }

    public static clientSideIdToUserIdHashId(clientSideId: string): IUserIdHashId {
        const key = atob(clientSideId);
        // as the key is constructed by concatenating two uuids (same length)
        // we can just split it in half
        const mid = key.length / 2;

        return {
            hashId: key.substring(0, mid),
            userId: key.substring(mid)
        }
    }
}

export default UploadedVideo;