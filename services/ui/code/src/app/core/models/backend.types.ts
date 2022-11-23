import { HttpResponse } from '@angular/common/http';

export interface BackendConfig {
    url: string;
}

export interface UploadSignatures {
    url: string;
    signatures: any;
}

export interface VideoUploadConfig {
    valid_file_types: string[],
    max_size_in_bytes: number
}

interface UploadProgress {
    type: number,
    loaded: number,
    total: number
}

export type UploadResponse = UploadProgress | HttpResponse<any>
