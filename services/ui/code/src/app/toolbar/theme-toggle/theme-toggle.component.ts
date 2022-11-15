import { Component } from '@angular/core';
import { ThemeService } from '../../core/services/theme.service';
import { faSun, faMoon } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-theme-toggle',
  templateUrl: './theme-toggle.component.html',
  styleUrls: ['./theme-toggle.component.scss']
})
export class ThemeToggleComponent {
  readonly faSun = faSun;
  readonly faMoon = faMoon;

  constructor(private themeService: ThemeService) { }

  public toggle(): void {
    this.themeService.toggle();
  }
}

