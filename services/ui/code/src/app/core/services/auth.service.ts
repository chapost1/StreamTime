import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable()
export class AuthService {
    private _isAuthenticated = new BehaviorSubject<boolean>(false);
    isAuthenticated = this._isAuthenticated.asObservable();

    public authenticate() {
        this._isAuthenticated.next(true);
    }

    public logout() {
        this._isAuthenticated.next(false);
    }
}
