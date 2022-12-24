import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, concatMap, tap, map, throwError, catchError } from 'rxjs';
import { HttpClient, HttpBackend, HttpRequest, HttpErrorResponse, HttpStatusCode } from '@angular/common/http';
import { AuthService } from './auth.service';
import { IBackendConfig } from '../models/backend/backend.types';
import { IUploadConfig, IUploadResponse, IUploadSignatures } from '../models/backend/upload.types';
import UploadConfig from '../models/entities/upload-config';
import { IUserVideosList, IVideosPage, IWatchVideoRecord } from '../models/backend/videos.types';
import UserVideosList from '../models/entities/videos/user-videos-list';
import { IUserIdHashId } from '../models/entities/videos/uploaded-video';
import WatchVideoRecord from '../models/entities/videos/watch-video-record';
import VideosPage from '../models/entities/videos/videos-page';

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
            }),
            catchError(this.handleError)
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
        return this.getVideoUploadInstructions(file.type, file.name).pipe(
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
        ).pipe(catchError(this.handleError));
    }

    private getVideoUploadInstructions(fileType: string, fileName: string): Observable<IUploadSignatures> {
        const urlToGetUploadInstructions = `${this.hostUrl}/${this.videoEndpointsRoute}/upload/`;
        const options = {
            params: {
                file_content_type: fileType,
                file_name: fileName
            }
        };

        return <Observable<IUploadSignatures>>this.httpClient.get(urlToGetUploadInstructions, options)
            .pipe(
                map((object: object) => {
                    return <IUploadSignatures>object
                }),
                catchError(this.handleError)
            );
    }

    public getAuthenticatedUserVideos(): Observable<UserVideosList> {
        const url = `${this.hostUrl}/${this.videoEndpointsRoute}/my/`;

        return <Observable<UserVideosList>>this.httpClient.get(url)
            .pipe(
                map((object: object) => {
                    return UserVideosList.fromInterface(<IUserVideosList>object);
                }),
                catchError(this.handleError)
            );
    }

    public deleteVideo(hashId: string): Observable<Object> {
        const url = `${this.hostUrl}/${this.videoEndpointsRoute}/my/${hashId}`;
        return this.httpClient.delete(url).pipe(catchError(this.handleError));
    }

    public updateVideo(hashId: string, data: {
        title?: string,
        description?: string,
        isPrivate?: boolean
    }): Observable<Object> {
        const url = `${this.hostUrl}/${this.videoEndpointsRoute}/my/${hashId}`;

        const payload = {
            title: data.title,
            description: data.description,
            is_private: data.isPrivate
        };

        return this.httpClient.put(url, payload).pipe(catchError(this.handleError));
    }

    public getWatchVideoRecord(identifiers: IUserIdHashId): Observable<WatchVideoRecord> {
        const url = `${this.hostUrl}/${this.videoEndpointsRoute}/watch`;
        const options = {
            params: {
                user_id: identifiers.userId,
                hash_id: identifiers.hashId
            }
        }
        return <Observable<WatchVideoRecord>>this.httpClient.get(url, options)
            .pipe(
                map((object: object) => {
                    return WatchVideoRecord.fromInterface(<IWatchVideoRecord>object);
                }),
                catchError(this.handleError)
            );
    }

    public exploreVideos(next: string | null): Observable<VideosPage> {
        const url = `${this.hostUrl}/${this.videoEndpointsRoute}/explore`;
        const options: any = {
            params: {
                include_my: 'true'
            }
        }
        if (next) {
            options.params['next'] = next;
        }
        return <Observable<VideosPage>>this.httpClient.get(url, options)
            .pipe(
                map((object: object) => {
                    return VideosPage.fromInterface(<IVideosPage>object);
                }),
                catchError(this.handleError)
            );
    }

    private handleError(err: HttpErrorResponse): Observable<Error> {
        let errorMessage: string = 'unknown error';

        if (err.status === 0) {
            // A client-side or network error occurred. Handle it accordingly.
            console.error(err.error);
            errorMessage = `An error occurred: ${err.statusText}`;
        } else {
            console.error(err.message);
            // The backend returned an unsuccessful response code.
            if (err.status < 500) {
                switch (err.status) {
                    case HttpStatusCode.BadRequest:
                    case HttpStatusCode.UnprocessableEntity:
                    case HttpStatusCode.PayloadTooLarge: {
                        errorMessage = 'Bad Request';
                        if (err.error) {
                            const {error, message} = err.error;
                            errorMessage = error || message || errorMessage;
                        }
                        break;
                    }
                    case HttpStatusCode.Unauthorized:
                    case HttpStatusCode.Forbidden: {
                        errorMessage = 'Access Denied';
                        break;
                    }
                    case HttpStatusCode.NotFound: {
                        errorMessage = 'Not Found';
                        break;
                    }
                    case HttpStatusCode.TooEarly: {
                        errorMessage = 'Too early, try later';
                        break;
                    }
                    default: {
                        errorMessage = 'Something went wrong';
                    }
                }
            } else {
                errorMessage = `internal server error: ${err.status}`;
            }
        }

        console.log(errorMessage);
        return throwError(() => new Error(errorMessage));
    }
}
