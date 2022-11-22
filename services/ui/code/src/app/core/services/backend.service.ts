import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, concatMap, tap, map } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { AuthService } from './auth.service';
import { NgToastStackService } from 'ng-toast-stack';
import { ObservableWrapper } from 'src/app/common/utils';

@Injectable()
export class BackendService {
    private _videoUploadConfig = new BehaviorSubject<VideoUploadConfig | undefined>(undefined);

    private config: BackendConfig | undefined = undefined;
    private readonly videoEndpointsRoute = 'video';

    constructor(
        private authService: AuthService,
        private httpClient: HttpClient,
        private toast: NgToastStackService
    ) {
        // this.authService.logout();// todo: remove this dummy call
        this.authService.authenticate();// todo: remove this dummy call
    }

    private get hostUrl(): string {
        return <string>this.config?.url;
    }

    public get videoUploadConfig(): Observable<VideoUploadConfig | undefined> {
        const config = this._videoUploadConfig.getValue();
        if (config) {
            return this._videoUploadConfig.asObservable();
        }
        // return this._videoUploadConfig.asObservable();
        const url = `${this.hostUrl}/${this.videoEndpointsRoute}/upload/config`;
        return <Observable<VideoUploadConfig>>this.httpClient.get(url).pipe(
            tap((conf: object) => {
                this._videoUploadConfig.next(<VideoUploadConfig>conf)
            }),
            map((conf: object) => {
                return conf;
            })
        );
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