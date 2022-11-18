import { Component } from '@angular/core';
import { Observable, map, BehaviorSubject } from 'rxjs';
import { ROUTES_CONFIG, RouteConfig } from '../common/routing-policy';
import { AuthService } from '../core/services/auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {
  private hideNavItemResolver = new BehaviorSubject<boolean>(false);
  private displayNavItemResolver = new BehaviorSubject<boolean>(true);
  public showCollapsedNavigationPanel: boolean = false;

  public navigations: Array<RouteConfig> = [
    ROUTES_CONFIG.LOG_IN,
    ROUTES_CONFIG.WORKSPACE,
    ROUTES_CONFIG.EXPLORE
  ];

  constructor(public authService: AuthService) { }

  public toggleNavigationPanel(): void {
    this.showCollapsedNavigationPanel = !this.showCollapsedNavigationPanel;
  }

  public shouldBeVisible(navigation: RouteConfig): Observable<boolean> {
    // hide in any case
    if (!navigation.navigationBarVisibility) {
      return this.hideNavItemResolver;
    }
    // if auth is required - depend on authentication
    if (navigation.isAuthenticationNeeded) {
      return this.authService.isAuthenticated;
    }
    // if auth is not allowed - depend on inversed authentication
    else if (!navigation.visibleToAuthenticatedUsers) {
      return this.authService.isAuthenticated.pipe(map(x => !x));
    } else {
      // visible to anyone
      return this.displayNavItemResolver;
    }
  }
}
