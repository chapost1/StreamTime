import { Component, OnInit, AfterContentChecked } from '@angular/core';
import { Observable } from 'rxjs';
import { AuthService } from './core/services/auth.service';
import { BackendService } from './core/services/backend.service';
import { ThemeService } from './core/services/theme.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, AfterContentChecked {
  public isDarkTheme: Observable<boolean>;
  public title: string = 'stream-time';
  public creator: string = 'Shahar Tal';
  public isAppReady: boolean = false;
  private initTS: number = -1;

  constructor(
    private themeService: ThemeService,
    private backendService: BackendService,
    private authService: AuthService
  ) {
    this.isDarkTheme = this.themeService.isDarkTheme;
  }

  ngAfterContentChecked() {
    this.themeService.initTheme();
  }

  ngOnInit() {
    // this.authService.logout();// todo: remove this dummy call
    this.authService.authenticate();// todo: remove this dummy call
    this.initTS = Date.now();
    this.backendService.initConfig(
      this.onBackendConfigRetrieval.bind(this)
    );
  }

  private onBackendConfigRetrieval(status: boolean): void {
    if (!status) {
      // raise an error snackbar
      return;
    }

    this.displayLogoForOneSecSinceInit(
      this.markAppAsReady.bind(this)
    );
  }

  private displayLogoForOneSecSinceInit(then: Function): void {
    const now = Date.now();
    const oneSec = 1000 * 1;
    const deltaUntilOneSecSinceInit = // avoid negatives
      Math.max(0, this.initTS + oneSec - now);
    setTimeout(then, deltaUntilOneSecSinceInit);
  }

  private markAppAsReady(): void {
    this.isAppReady = true;
  }
}
