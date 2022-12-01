import { Injectable, OnDestroy } from "@angular/core";
import { Observable, Observer } from 'rxjs';
import { AnonymousSubject } from 'rxjs/internal/Subject';
import { Subject } from 'rxjs';
import { map } from 'rxjs/operators';
import { BackendService } from "./backend.service";
import { NgToastStackService } from "ng-toast-stack";
import { AuthService } from "./auth.service";

@Injectable()
export class UploadedVideosSyncService implements OnDestroy {
    private url: string;
    private subject: AnonymousSubject<MessageEvent> | undefined;
    private ws: WebSocket | undefined;
    public syncCalls: Subject<string>;

    constructor(
        private backendService: BackendService,
        private toast: NgToastStackService,
        private authService: AuthService
    ) {
        this.url = this.backendService.videosSyncWSURL;
       
        this.syncCalls = <Subject<string>>this.connect(this.url).pipe(
            map(
                (response: MessageEvent): string => {
                    return JSON.parse(response.data);
                }
            )
        );
    }

    ngOnDestroy() {
        this.closeConnection();
    }

    public connect(url: string): AnonymousSubject<MessageEvent> {
        if (!this.subject) {
            this.subject = this.create(url);
        }
        return this.subject;
    }

    private closeConnection(): void {
        if (this.ws?.OPEN) {
            this.ws?.close();
        }
    }

    private create(url: string): AnonymousSubject<MessageEvent> {
        const params = {user_id: this.authService.getAuthenticatedUserId()};
        this.ws = new WebSocket(`${url}?${new URLSearchParams(params).toString()}`);

        const observable = new Observable((obs: Observer<MessageEvent>) => {
            (<WebSocket>this.ws).onmessage = obs.next.bind(obs);
            (<WebSocket>this.ws).onerror = obs.error.bind(obs);
            (<WebSocket>this.ws).onclose = obs.complete.bind(obs);
            return (<WebSocket>this.ws).close.bind((<WebSocket>this.ws));
        });
        const observer = {
            error: (error: any) => {
                this.toast.error(error);
            },
            complete: () => {
                console.error('websocket connection has been closed');
            },
            next: (data: Object) => {
                if (this.ws?.readyState === WebSocket.OPEN) {
                    this.ws?.send(JSON.stringify(data));
                }
            }
        };
        return new AnonymousSubject<MessageEvent>(observer, observable);
    }
}
