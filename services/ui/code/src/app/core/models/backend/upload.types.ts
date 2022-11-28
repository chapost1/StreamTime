import { HttpResponse } from '@angular/common/http';

export type IUploadSignatures = {
    url: string;
    signatures: any;
}

export type IUploadConfig = {
    valid_file_types: string[],
    max_size_in_bytes: number
}

export type IUploadProgress = {
    type: number,
    loaded: number,
    total: number
}

export type IUploadResponse = IUploadProgress | HttpResponse<any>