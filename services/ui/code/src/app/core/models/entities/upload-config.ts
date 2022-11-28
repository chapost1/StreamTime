import { IUploadConfig } from "../backend/upload.types";

class UploadConfig {
    public validFileTypes: string[] = [];
    public maxSizeInBytes: number = 0;

    constructor(validFileTypes: string[], maxSizeInBytes: number) {
        this.validFileTypes = validFileTypes || [];
        this.maxSizeInBytes = maxSizeInBytes || 0;
    }

    static fromInterface(source: IUploadConfig): UploadConfig {
        return new UploadConfig(
            source.valid_file_types,
            source.max_size_in_bytes
        )
    }

    public toInterface(): IUploadConfig {
        return {
            valid_file_types: this.validFileTypes,
            max_size_in_bytes: this.maxSizeInBytes
        }
    }
}

export default UploadConfig;