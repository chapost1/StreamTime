import { Component, OnInit, AfterContentChecked } from '@angular/core';
import { Observable } from 'rxjs';
import { BackendService } from './core/services/backend.service';
import { ThemeService } from './core/services/theme.service';

import { NgToastStackService } from 'ng-toast-stack';

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

  public appIsDown: boolean = false;

  public showProgressBarWhileAppIsNotReady: boolean = true;

  private initTS: number = -1;


  constructor(
    private themeService: ThemeService,
    private backendService: BackendService,
    private toast: NgToastStackService
  ) {
    this.isDarkTheme = this.themeService.isDarkTheme;
  }

  ngAfterContentChecked() {
    this.themeService.initTheme();
  }

  ngOnInit() {
    this.initTS = Date.now();
    this.backendService.initConfig(
      this.onBackendConfigRetrieval.bind(this)
    );
  }

  private onBackendConfigRetrieval(status: boolean): void {
    if (!status) {
      this.appIsDown = true;
      this.toast.error({
        msg: 'internal server error, please try again later',
        autoClose: false
      });
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
