import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styles: []
})
export class AppComponent implements OnInit {
  title: string = 'stream-time';
  backendUrl: string = '';

  ngOnInit() {
    fetch('./assets/backend.json').then(res => res.json())
      .then(backendDataJson => {
        this.backendUrl = backendDataJson.url;
      });
  }
}
