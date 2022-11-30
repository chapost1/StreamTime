import { Component, EventEmitter, Input, Output } from '@angular/core';
import Video from 'src/app/core/models/entities/videos/video';
import { faPen, faPlay, faTrashCan } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-video-summary',
  templateUrl: 'video-summary.component.html',
  styleUrls: ['video-summary.component.scss']
})
export class VideoSummaryComponent {
  @Output() deleteVideoEmitter: EventEmitter<Video> = new EventEmitter<Video>();
  @Input() video: Video | undefined;

  public icons = {
    edit: faPen,
    watch: faPlay,
    delete: faTrashCan
  }

  public onDelete(video: Video): void {
    this.deleteVideoEmitter.emit(video);
  }
}
