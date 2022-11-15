import { Injectable, OnInit } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable()
export class ThemeService {
  private readonly localStorageThemeSettings = 'isDarkTheme';
  private _darkTheme = new Subject<boolean>();
  isDarkTheme = this._darkTheme.asObservable();

  initTheme() {
    debugger;
    const isDarkTheme = localStorage.getItem(this.localStorageThemeSettings);
    debugger;
    if (isDarkTheme) {
      this.setDarkTheme(Boolean(isDarkTheme));
    }
  }

  setDarkTheme(isDarkTheme: boolean): void {
    this._darkTheme.next(isDarkTheme);
    localStorage.setItem(this.localStorageThemeSettings, String(isDarkTheme));
  }
}
