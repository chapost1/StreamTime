import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { Observable, Subscriber } from 'rxjs';
import { ObservableWrapper } from '../../common/utils';
import { ROUTES_CONFIG } from 'src/app/common/routing-policy';

import { NgToastStackService } from 'ng-toast-stack';

@Injectable()
export class AuthGuard implements CanActivate {
    
    constructor(
        private authService: AuthService,
        private router: Router,
        private toast: NgToastStackService
    ) { };

    canActivate(next: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> {
        return new Observable<boolean>((observer: Subscriber<boolean>) => {
            const nextPath = next.routeConfig?.path || '';
            this.handler.call(this, observer, nextPath);
        });
    }

    private async handler(observer: Subscriber<boolean>, nextPath: string) {
        const letUserPass = await this.getAuthenticationApprovement();
        const loginPath = ROUTES_CONFIG.LOG_IN.path;
        if (!letUserPass && nextPath !== loginPath) {
            this.router.navigateByUrl(`/${loginPath}`);
        }
        observer.next(letUserPass);
        observer.complete();
    }

    private async getAuthenticationApprovement(): Promise<boolean> {
        const { error, data: isAuthenticated } = await ObservableWrapper(
            this.authService.isAuthenticated
        );
        let approvement = isAuthenticated;
        if (error) {
            approvement = false;
            console.error(error);

            this.toast.error('unauthorized');
        }
        return approvement;
    }
}