import { Component, OnDestroy, OnInit } from '@angular/core';
import { faSquarePlus } from '@fortawesome/free-solid-svg-icons';
import { MatDialog } from '@angular/material/dialog';
import { UploadVideoDialog } from './upload-video-dialog/upload-video-dialog.component';
import { Subscription } from 'rxjs';
import { BackendService } from 'src/app/core/services/backend.service';
import { NgToastStackService } from 'ng-toast-stack';
import { UserVideosList } from 'src/app/core/models/entities/videos/types';
import UploadedVideo from 'src/app/core/models/entities/videos/uploaded-video';
import UnprocessedVideo from 'src/app/core/models/entities/videos/unprocessed-video';
import Video from 'src/app/core/models/entities/videos/video';

@Component({
  selector: 'app-workspace',
  templateUrl: './workspace.component.html',
  styleUrls: ['./workspace.component.scss']
})
export class WorkspaceComponent implements OnInit, OnDestroy {
  private subscriptions: Subscription = new Subscription();
  public icons = {
    createPlusIcon: faSquarePlus
  }

  public fetchingUserVideosList: boolean = false;
  public userVideosList: UserVideosList = {
    unprocessedVideos: [],
    videos: []
  }

  constructor(
    public dialog: MatDialog,
    private backendService: BackendService,
    private toast: NgToastStackService
  ) { }

  ngOnInit(): void {
    // todo:
    // open WS connection

    this.initUserVideosList();
  }

  ngOnDestroy(): void {
    // todo:
    // close WS connection

    this.subscriptions.unsubscribe();
  }

  private async initUserVideosList(): Promise<void> {
    this.fetchingUserVideosList = true;
    await this.fetchUserVideosList();
    this.fetchingUserVideosList = false;
  }

  private fetchUserVideosList(): Promise<void> {
    return new Promise(resolve => {
      const sub = this.backendService.getAuthenticatedUserVideos()
        .subscribe({
          next: (userVideosList) => {
            this.userVideosList = userVideosList;
          },
          error: (e) => {
            this.toast.error(e);
          },
          complete: resolve
        });

      this.subscriptions.add(sub);
    })
  }

  public onDelete(video: UploadedVideo): void {
    this.deleteVideo(video.hashId, (success: boolean) => {
      if (!success) {
        return;
      }
      const list: UploadedVideo[] = this.getVideoListByVideoType(video);
      this.clearVideoFromUserList(list, video.hashId);
    });
  }

  private getVideoListByVideoType(video: UploadedVideo): UploadedVideo[] {
    if (video instanceof UnprocessedVideo) {
      return this.userVideosList.unprocessedVideos;
    } else if (video instanceof Video) {
      return this.userVideosList.videos;
    }
    return [];
  }

  private clearVideoFromUserList(list: UploadedVideo[], hashId: string): void {
    const idx = list.findIndex(video => video.hashId === hashId);
    if (idx < 0) {
      return;
    }
    list.splice(idx, 1);
  }

  public deleteVideo(hashId: string, then: Function): void {
    const sub = this.backendService.deleteVideo(hashId)
      .subscribe({
        next: () => {
          then(true);
        },
        error: (e) => {
          this.toast.error(e);
          then(false);
        }
      });

    this.subscriptions.add(sub);
  }

  public openUploadVideoDialog() {
    this.dialog.open(UploadVideoDialog, {
      autoFocus: false,
      height: 'auto',
      minWidth: 'calc(100% - 2rem)',
      disableClose: true,
      exitAnimationDuration: '200ms'
    });
  }
}
