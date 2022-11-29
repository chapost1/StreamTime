import { Component, Input } from '@angular/core';
import { UserVideosList } from 'src/app/core/models/entities/videos/types';
import { faEye, faEyeSlash, faBars, faList } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-uploaded-videos',
  templateUrl: 'uploaded-videos.component.html',
  styleUrls: ['uploaded-videos.component.scss']
})
export class UploadedVideosComponent {
  @Input() userVideosList: UserVideosList | undefined = undefined;

  public icons = {
    public: faEye,
    private: faEyeSlash,
    draft: faBars,
    listed: faList
  }

  public isUserVideosListNotEmpty(): boolean {
    return typeof this.userVideosList !== 'undefined' &&
      (0 < this.userVideosList.unprocessedVideos.length || 0 < this.userVideosList.videos.length);
  }

  public unprocessedVideosDisplayedColumns(): string[] {
    return ['videoSummary', 'failureReason', 'uploadTime'];
  }
}
