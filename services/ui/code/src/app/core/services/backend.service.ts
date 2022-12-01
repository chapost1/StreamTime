import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, concatMap, tap, map } from 'rxjs';
import { HttpClient, HttpBackend, HttpRequest } from '@angular/common/http';
import { AuthService } from './auth.service';
import { IBackendConfig } from '../models/backend/backend.types';
import { IUploadConfig, IUploadResponse, IUploadSignatures } from '../models/backend/upload.types';
import UploadConfig from '../models/entities/upload-config';
import { IUserVideosList } from '../models/backend/videos.types';
import UserVideosList from '../models/entities/videos/user-videos-list';

@Injectable()
export class BackendService {
    private _videoUploadConfig = new BehaviorSubject<UploadConfig | undefined>(undefined);

    private config: IBackendConfig | undefined = undefined;
    private readonly videoEndpointsRoute = 'video';

    constructor(
        private authService: AuthService,
        private httpClient: HttpClient,
        private handler: HttpBackend
    ) {
        // this.authService.logout();// todo: remove this dummy call
        this.authService.authenticate();// todo: remove this dummy call
    }

    private get hostUrl(): string {
        return <string>this.config?.url;
    }

    public get videosSyncWSURL(): string {
        return <string>this.config?.client_videos_sync_wss;
    }

    public get videoUploadConfig(): Observable<UploadConfig | undefined> {
        const config = this._videoUploadConfig.getValue();
        if (config) {
            return this._videoUploadConfig.asObservable();
        }
        const url = `${this.hostUrl}/${this.videoEndpointsRoute}/upload/config`;
        return <Observable<UploadConfig>>this.httpClient.get(url).pipe(
            tap((conf: object) => {
                this._videoUploadConfig.next(UploadConfig.fromInterface(<IUploadConfig>conf))
            }),
            map((conf: object) => {
                return UploadConfig.fromInterface(<IUploadConfig>conf);
            })
        );
    }

    public initConfig(callback: Function): void {
        if (typeof this.config != 'undefined') {
            return callback(true);
        }
        fetch('./assets/backend.json').then(res => res.json())
            .then((backendDataJson: IBackendConfig) => {
                this.config = backendDataJson;
                callback(true);
            })
            .catch(err => {
                console.log('internal server error, couldn\'t get backend config');
                console.error(err);
                callback(false);
            });
    }

    public uploadVideoFile(file: File): Observable<IUploadResponse> {
        return this.getVideoUploadInstructions(file.type).pipe(
            // use concatMap to make sure you make the second call after the first one completes
            concatMap((instructions: IUploadSignatures) => {
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

    private uploadFileUsingInstuctioctions(file: File, instructions: IUploadSignatures): Observable<IUploadResponse> {
        const payload = this.createSignedPayloadToUploadFile(file, instructions.signatures);

        // use new http client to use newly reset-ed headers
        return <Observable<IUploadResponse>>new HttpClient(this.handler).request(
            new HttpRequest('POST', instructions.url, payload, { reportProgress: true })
        );
    }

    private getVideoUploadInstructions(fileType: string): Observable<IUploadSignatures> {
        const urlToGetUploadInstructions = `${this.hostUrl}/${this.videoEndpointsRoute}/upload/`;
        const options = {
            params: {
                file_content_type: fileType
            }
        };

        return <Observable<IUploadSignatures>>this.httpClient.get(urlToGetUploadInstructions, options);
    }

    public getAuthenticatedUserVideos(): Observable<UserVideosList> {
        const url = `${this.hostUrl}/${this.videoEndpointsRoute}/my/`;

        return <Observable<UserVideosList>>this.httpClient.get(url)
            .pipe(
                map((object: object) => {
                    return UserVideosList.fromInterface(<IUserVideosList>object);
                })
            );
    }

    public deleteVideo(hashId: string): Observable<Object> {
        const url = `${this.hostUrl}/${this.videoEndpointsRoute}/my/${hashId}`;
        return this.httpClient.delete(url);
    }
}
