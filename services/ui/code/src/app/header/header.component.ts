import { Component } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {
  public showCollapsedNavigationPanel: boolean = false;

  public toggleNavigationPanel() {
    this.showCollapsedNavigationPanel = !this.showCollapsedNavigationPanel;
  }
}
