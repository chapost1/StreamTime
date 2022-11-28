import { IUploadedVideo } from "../../backend/videos.types";
import assertField from "../assert-field";

class UploadedVideo {
    hashId: string;
    userId: string;
    uploadTime: string;

    protected constructor(hashId: string, userId: string, uploadTime: string) {
        assertField(this.constructor.name, 'hashId', hashId);
        this.hashId = hashId;
        assertField(this.constructor.name, 'userId', userId);
        this.userId = userId;
        assertField(this.constructor.name, 'uploadTime', uploadTime);
        this.uploadTime = uploadTime;
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
}

export default UploadedVideo;