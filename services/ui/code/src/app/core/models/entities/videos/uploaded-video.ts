import { IUploadedVideo } from "../../backend/videos.types";
import assertField from "../assert-field";

export interface IUserIdHashId {
    hashId: string;
    userId: string;
}

const IUserIdHashIdSeperator = '$';

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
        return btoa(`${this.hashId}${IUserIdHashIdSeperator}${this.userId}`)
    }

    public static clientSideIdToUserIdHashId(clientSideId: string): IUserIdHashId {
        const key = atob(clientSideId).split(IUserIdHashIdSeperator)

        return {
            hashId: key[0],
            userId: key[1]
        }
    }
}

export default UploadedVideo;