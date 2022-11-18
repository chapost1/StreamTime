import { Injectable } from '@angular/core';

export interface BackendConfig {
    url: string;
}

@Injectable()
export class BackendService {
    private config: BackendConfig | undefined = undefined;

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
}
