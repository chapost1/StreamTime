import { Component } from '@angular/core';
import { ThemeService } from '../core/services/theme.service';
import { faSun, faMoon } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector:'app-toolbar',
  templateUrl:'./toolbar.component.html',
  styleUrls: ['./toolbar.component.scss']
})
export class ToolbarComponent {
  faSun = faSun;
  faMoon = faMoon;
  isDarkTheme: boolean;

  constructor(private themeService: ThemeService) {
    this.isDarkTheme = false;
    this.themeService.isDarkTheme.subscribe(this.onThemeChange.bind(this));
  }

  onThemeChange(isDarkTheme: boolean) {
    debugger;
    console.log(isDarkTheme);
    this.isDarkTheme = isDarkTheme || false;
    console.log(this.isDarkTheme)
  }

  toggleDarkTheme() {
    debugger;
    const isDarkTheme: boolean = !this.isDarkTheme;
    this.themeService.setDarkTheme(isDarkTheme);
  }
}
