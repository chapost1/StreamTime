import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

const TEMP_CONSTANT_USER_ID = 'ae6d14eb-d222-4967-98d9-60a7cc2d7891';

@Injectable()
export class AuthService {
    private _isAuthenticated = new BehaviorSubject<boolean>(false);
    public isAuthenticated = this._isAuthenticated.asObservable();

    public authenticate() {
        this._isAuthenticated.next(true);
    }

    public logout() {
        this._isAuthenticated.next(false);
    }

    public getAuthenticatedUserId(): string {
        return TEMP_CONSTANT_USER_ID;
    }
}
