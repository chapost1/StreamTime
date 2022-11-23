import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { Observable, tap, map, catchError, throwError } from 'rxjs';
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
        const nextPath = next.routeConfig?.path || '';
        const loginPath = ROUTES_CONFIG.LOG_IN.path;
        const isAimingLoginPath = nextPath === loginPath
        return this.authService.isAuthenticated.pipe(
            tap((isAuthenticated: boolean) => {
                if (!isAuthenticated && !isAimingLoginPath) {
                    this.router.navigateByUrl(`/${loginPath}`);
                }

            }),
            map((isAuthenticated: boolean) => isAuthenticated),
            catchError((error: any, caught: Observable<boolean>): Observable<never> => {
                // display error
                console.error(error);
                this.toast.error('unauthorized');
                // navigate to somewhere else
                this.router.navigateByUrl(`/`);
                // re-throw
                return throwError(() => error);
            })
        );
    }
}