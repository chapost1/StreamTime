import { HttpResponse } from '@angular/common/http';

export type BackendConfig = {
    url: string;
}

export type UploadSignatures = {
    url: string;
    signatures: any;
}

export type VideoUploadConfig = {
    valid_file_types: string[],
    max_size_in_bytes: number
}

export type UploadProgress = {
    type: number,
    loaded: number,
    total: number
}

export type UploadResponse = UploadProgress | HttpResponse<any>
