import { Component } from '@angular/core';
import { faCompass, faVideo } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {
  public faCompass = faCompass;
  public faVideo = faVideo;

  public showCollapsedNavigationPanel: boolean = false;

  public toggleNavigationPanel() {
    this.showCollapsedNavigationPanel = !this.showCollapsedNavigationPanel;
  }
}
