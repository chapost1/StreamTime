import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { AuthGuard } from './auth-guard';
import { Observable, map, tap } from 'rxjs';

@Injectable()
export class NegateAuthGuard implements CanActivate {

    constructor(
        private authGuard: AuthGuard,
        private router: Router
    ) { };

    canActivate(next: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> {
        return this.authGuard.canActivate(next, state).pipe(
            // do not let authenticated user pass through, redirect to default route
            tap(isAuthenticated => {
                if (isAuthenticated) {
                    this.router.navigateByUrl(`/`);
                }
            }),
            // inverse the authGuard result, so authenticated means false
            map(result => !result)
        );
    }
}