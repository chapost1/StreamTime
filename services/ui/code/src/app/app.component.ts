import { Component, OnInit, AfterContentChecked } from '@angular/core';
import { Observable } from 'rxjs';
import { ThemeService } from './core/services/theme.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, AfterContentChecked {
  isDarkTheme: Observable<boolean>;
  title: string = 'stream-time';
  backendUrl: string = '';

  constructor(private themeService: ThemeService) {
    this.isDarkTheme = this.themeService.isDarkTheme;
  }

  ngAfterContentChecked() {
    this.themeService.initTheme();
  }

  ngOnInit() {
    fetch('./assets/backend.json').then(res => res.json())
      .then(backendDataJson => {
        this.backendUrl = backendDataJson.url;
      });
  }
}
