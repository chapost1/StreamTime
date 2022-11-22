import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable()
export class ThemeService {
  private readonly localStorageThemeSettings = 'isDarkTheme';
  private _darkTheme = new Subject<boolean>();
  public isDarkTheme = this._darkTheme.asObservable();

  public initTheme() {
    this.setTheme(this.getTheme());
  }

  public toggle() {
    this.setTheme(!this.getTheme());
  }

  private getTheme(): boolean {
    const isDarkTheme = localStorage.getItem(this.localStorageThemeSettings);
    if (isDarkTheme) {
      return isDarkTheme === 'true';
    } else {
      return true;
    }
  }

  private setTheme(isDarkTheme: boolean): void {
    this._darkTheme.next(isDarkTheme);
    localStorage.setItem(this.localStorageThemeSettings, String(isDarkTheme));
  }
}