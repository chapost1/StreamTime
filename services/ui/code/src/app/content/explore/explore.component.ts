import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-explore',
  template: `
  <app-content-padding>
    <p>
      explore works!
    </p>
  </app-content-padding>
  `,
  styles: [
  ]
})
export class ExploreComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

}
