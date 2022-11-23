import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable()
export class ThemeService {
  private readonly localStorageThemeSettings = 'isDarkTheme';
  private _darkThemeSubject = new Subject<boolean>();
  public isDarkTheme = this._darkThemeSubject.asObservable();

  public initTheme() {
    this._isDarkTheme = this._isDarkTheme;
  }

  public toggle() {
    this._isDarkTheme = !this._isDarkTheme;
  }

  private get _isDarkTheme(): boolean {
    const isDarkTheme: string | null = localStorage.getItem(this.localStorageThemeSettings);
    if (typeof isDarkTheme === 'string') {
      return isDarkTheme.toBoolean();
    } else {
      // default to true
      return true;
    }
  }

  private set _isDarkTheme(isDarkTheme: boolean) {
    this._darkThemeSubject.next(isDarkTheme);
    localStorage.setItem(this.localStorageThemeSettings, isDarkTheme.toString());
  }
}
