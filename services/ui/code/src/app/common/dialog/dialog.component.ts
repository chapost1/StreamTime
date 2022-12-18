import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { ThemeService } from '../../core/services/theme.service';

@Component({
  selector: 'app-dialog',
  template: `
  <div [class]="(isDarkTheme | async)? 'dark-theme': 'light-theme'">
    <mat-card>
      <ng-content></ng-content>
    </mat-card>
  </div>`
})
export class AppDialogComponent {
  public isDarkTheme: Observable<boolean>;
  constructor(private themeService: ThemeService) {
    this.isDarkTheme = this.themeService.isDarkTheme;
  }
}
