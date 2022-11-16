import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

export interface BackendConfig {
    url: string;
}

@Injectable()
export class BackendService {
    private _configRetrievalEmitter = new Subject<boolean>();
    public configRetrievalEmitter = this._configRetrievalEmitter.asObservable();

    private config: BackendConfig | undefined;

    public initConfig() {
        fetch('../../assets/backend.json').then(res => res.json())
            .then((backendDataJson: BackendConfig) => {
                this.config = backendDataJson;
                this._configRetrievalEmitter.next(true);
            })
            .catch(err => {
                console.log('internal server error, couldn\'t get backend config');
                console.error(err);
                this._configRetrievalEmitter.next(false);
            });
    }
}
