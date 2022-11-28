import { Component, Input, OnInit } from '@angular/core';
import { UserVideosList } from 'src/app/core/models/entities/videos/types';

@Component({
  selector: 'app-uploaded-videos',
  templateUrl: 'uploaded-videos.component.html',
  styles: [
  ]
})
export class UploadedVideosComponent implements OnInit {
  @Input() userVideosList: UserVideosList | undefined = undefined;

  constructor() { }

  ngOnInit(): void {
  }

  public isUserVideosListNotEmpty(): boolean {
    return typeof this.userVideosList !== 'undefined' &&
      (0 < this.userVideosList.unprocessedVideos.length || 0 < this.userVideosList.videos.length);
  }

}
