import { Injectable } from '@angular/core';
import { Observable, concatMap } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { AuthService } from './auth.service';

export interface BackendConfig {
    url: string;
}

export interface UploadSignatures {
    url: string;
    signatures: any;
}

@Injectable()
export class BackendService {
    private config: BackendConfig | undefined = undefined;
    private readonly videoEndpointsRoute = 'video';

    constructor(
        private authService: AuthService,
        private httpClient: HttpClient
    ) {
        // this.authService.logout();// todo: remove this dummy call
        this.authService.authenticate();// todo: remove this dummy call
    }

    public initConfig(callback: Function): void {
        if (typeof this.config != 'undefined') {
            return callback(true);
        }
        fetch('./assets/backend.json').then(res => res.json())
            .then((backendDataJson: BackendConfig) => {
                this.config = backendDataJson;
                callback(true);
            })
            .catch(err => {
                console.log('internal server error, couldn\'t get backend config');
                console.error(err);
                callback(false);
            });
    }

    private get hostUrl(): string {
        return <string>this.config?.url;
    }

    public uploadVideoFile(file: File): Observable<any> {
        return this.getVideoUploadInstructions(file.type).pipe(
            // use concatMap to make sure you make the second call after the first one completes
            concatMap((instructions: UploadSignatures) => {
                return this.uploadFileUsingInstuctioctions(file, instructions);
            })
        );
    }

    private createSignedPayloadToUploadFile(file: File, signatures: any): FormData {
        const payload = new FormData();

        Object.keys(signatures || {}).forEach(key => {
            payload.append(key, signatures[key]);
        });

        payload.append('file', file);

        return payload;
    }

    private uploadFileUsingInstuctioctions(file: File, instructions: UploadSignatures): Observable<object> {
        const payload = this.createSignedPayloadToUploadFile(file, instructions.signatures);
        return this.httpClient.post(instructions.url, payload);
    }

    private getVideoUploadInstructions(fileType: string): Observable<UploadSignatures> {
        const urlToGetUploadInstructions = `${this.hostUrl}/${this.videoEndpointsRoute}/upload/`;
        const options = {
            params: {
                file_content_type: fileType
            }
        };

        return <Observable<UploadSignatures>>this.httpClient.get(urlToGetUploadInstructions, options);
    }
}
