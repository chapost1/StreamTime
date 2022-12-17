import { Component, EventEmitter, Input, Output } from '@angular/core';
import UserVideosList from 'src/app/core/models/entities/videos/user-videos-list';
import { faEye, faEyeSlash, faBars, faList } from '@fortawesome/free-solid-svg-icons';
import UploadedVideo from 'src/app/core/models/entities/videos/uploaded-video';

@Component({
  selector: 'app-uploaded-videos',
  templateUrl: 'uploaded-videos.component.html',
  styleUrls: ['uploaded-videos.component.scss']
})
export class UploadedVideosComponent {
  @Output() watchVideoEmitter: EventEmitter<UploadedVideo> = new EventEmitter<UploadedVideo>();
  @Output() editVideoEmitter: EventEmitter<UploadedVideo> = new EventEmitter<UploadedVideo>();
  @Output() deleteVideoEmitter: EventEmitter<UploadedVideo> = new EventEmitter<UploadedVideo>();
  @Output() uploadVideoEmitter: EventEmitter<void> = new EventEmitter<void>();
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

  public onDelete(video: UploadedVideo): void {
    this.deleteVideoEmitter.emit(video);
  }

  public onEdit(video: UploadedVideo): void {
    this.editVideoEmitter.emit(video);
  }

  public onWatch(video: UploadedVideo): void {
    this.watchVideoEmitter.emit(video);
  }

  public onUploadVideoClick(): void {
    this.uploadVideoEmitter.emit();
  }
}
