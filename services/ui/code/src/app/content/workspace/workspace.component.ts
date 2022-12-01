import { Component, OnDestroy, OnInit } from '@angular/core';
import { faSquarePlus } from '@fortawesome/free-solid-svg-icons';
import { MatDialog } from '@angular/material/dialog';
import { UploadVideoDialog } from './upload-video-dialog/upload-video-dialog.component';
import { Subscription } from 'rxjs';
import { BackendService } from 'src/app/core/services/backend.service';
import { NgToastStackService } from 'ng-toast-stack';
import UploadedVideo from 'src/app/core/models/entities/videos/uploaded-video';
import UserVideosList from 'src/app/core/models/entities/videos/user-videos-list';
import { UploadedVideosSyncService } from 'src/app/core/services/uploaded-videos-sync.service';

@Component({
  selector: 'app-workspace',
  templateUrl: './workspace.component.html',
  styleUrls: ['./workspace.component.scss'],
  providers: [UploadedVideosSyncService]
})
export class WorkspaceComponent implements OnInit, OnDestroy {
  private subscriptions: Subscription = new Subscription();
  public icons = {
    createPlusIcon: faSquarePlus
  }

  public fetchingUserVideosList: boolean = false;
  public userVideosList: UserVideosList = new UserVideosList();

  constructor(
    public dialog: MatDialog,
    private backendService: BackendService,
    private syncService: UploadedVideosSyncService,
    private toast: NgToastStackService
  ) { }

  ngOnInit(): void {
    this.connectUploadedVideosSyncCalls();
    this.initUserVideosList();
  }

  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
  }
  
  private connectUploadedVideosSyncCalls(): void {
    const sub = this.syncService.syncCalls?.subscribe({
      next: this.fetchUserVideosList.bind(this)
    });
    this.subscriptions.add(sub);
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
          next: userVideosList => {
            this.userVideosList = userVideosList;
          },
          error: (error: Error) => {
            this.toast.error(error.message);
          },
          complete: resolve
        });

      this.subscriptions.add(sub);
    })
  }

  public onDelete(video: UploadedVideo): void {
    const onSuccess = () => {
      this.userVideosList.removeVideo(video);
    }

    this.deleteVideo(video.hashId, onSuccess);
  }

  public deleteVideo(hashId: string, onSuccess: Function): void {
    const sub = this.backendService.deleteVideo(hashId)
      .subscribe({
        next: onSuccess.bind(this),
        error: (error: Error) => {
          this.toast.error(error.message);
        }
      });

    this.subscriptions.add(sub);
  }

  public onUploadVideoRequest(event: void): void {
    this.openUploadVideoDialog();
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
