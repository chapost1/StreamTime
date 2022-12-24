import { IUnprocessedVideo } from "../../backend/videos.types";
import UploadedVideo from "./uploaded-video";
import { removeUndefinedValuesKeysFromObject } from '../../../../common/utils';

class UnprocessedVideo extends UploadedVideo {
    failureReason: string | null;

    constructor(hashId: string, userId: string, fileName: string, uploadTime: string, failureReason: string | undefined) {
        super(hashId, userId, fileName, uploadTime);

        this.failureReason = failureReason || null;
    }

    public isStillProcessing(): boolean {
        return this.failureReason === null;
    }

    public isFailed(): boolean {
        return this.failureReason !== null;
    }

    static override fromInterface(source: IUnprocessedVideo): UnprocessedVideo {
        return new UnprocessedVideo(
            source.hash_id,
            source.user_id,
            source.file_name,
            source.upload_time,
            source.failure_reason
        )
    }

    public override toInterface(): IUnprocessedVideo {
        const result = {
            ...super.toInterface(),
            failure_reason: this.failureReason || undefined
        }
        removeUndefinedValuesKeysFromObject(result);
        return result;
    }
}

export default UnprocessedVideo;