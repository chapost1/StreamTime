import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { Observable, Subscriber } from 'rxjs';
import { ROUTES_CONFIG } from 'src/app/common/routing-policy';
import { ObservableWrapper } from '../../common/utils';

@Injectable()
export class UnAuthGuard implements CanActivate {
    constructor(private authService: AuthService, private router: Router) { };
    canActivate(next: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> {
        return new Observable<boolean>((observer: Subscriber<boolean>) => {
            this.handler.call(this, observer);
        });
    }

    private async handler(observer: Subscriber<boolean>) {
        const userIsAuthenticated = await this.getAuthenticationApprovement();
        if (userIsAuthenticated) {
            this.router.navigateByUrl(`/${ROUTES_CONFIG.EXPLORE.path}`);
        }
        observer.next(!userIsAuthenticated);
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
            // todo: actually handle it using snackbar or some special navigation page...
        }
        return approvement;
    }
}