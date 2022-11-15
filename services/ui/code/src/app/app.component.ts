import { Component, OnInit, AfterViewInit } from '@angular/core';
import { Observable } from 'rxjs';
import { ThemeService } from './core/services/theme.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styles: []
})
export class AppComponent implements OnInit, AfterViewInit {
  isDarkTheme: Observable<boolean>;
  title: string = 'stream-time';
  backendUrl: string = '';

  constructor(private themeService: ThemeService) {
    this.isDarkTheme = this.themeService.isDarkTheme;
  }

  ngAfterViewInit() {
    this.themeService.initTheme();
  }

  ngOnInit() {
    fetch('./assets/backend.json').then(res => res.json())
      .then(backendDataJson => {
        this.backendUrl = backendDataJson.url;
      });
  }
}
