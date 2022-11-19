import { Component } from '@angular/core';

@Component({
  selector: 'app-content-padding',
  template: `<div class="w-100 p-2">
    <ng-content></ng-content>
  </div>`,
  styles: [
  ]
})
export class ContentPaddingComponent {}
