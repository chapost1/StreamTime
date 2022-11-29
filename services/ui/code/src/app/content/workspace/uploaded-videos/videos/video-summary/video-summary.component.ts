import { Component, Input } from '@angular/core';
import Video from 'src/app/core/models/entities/videos/video';
import { faPen, faPlay, faTrashCan } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-video-summary',
  templateUrl: 'video-summary.component.html',
  styleUrls: ['video-summary.component.scss']
})
export class VideoSummaryComponent {
  @Input() video: Video | undefined;

  public icons = {
    edit: faPen,
    watch: faPlay,
    delete: faTrashCan
  }
}
