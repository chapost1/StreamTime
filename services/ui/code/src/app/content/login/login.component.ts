import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-login',
  template: `
  <app-content-padding>
    <p>
      login works!
    </p>
  </app-content-padding>
  `,
  styles: [
  ]
})
export class LoginComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

}
