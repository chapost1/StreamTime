import { Component, OnDestroy, OnInit } from '@angular/core';
import { faSquarePlus } from '@fortawesome/free-solid-svg-icons';
import { MatDialog } from '@angular/material/dialog';
import { UploadVideoDialog } from './upload-video-dialog/upload-video-dialog.component';
import { Subscription } from 'rxjs';
import { BackendService } from '../../core/services/backend.service';
import { NgToastStackService } from 'ng-toast-stack';
import UploadedVideo from '../../core/models/entities/videos/uploaded-video';
import UserVideosList from '../../core/models/entities/videos/user-videos-list';
import { UploadedVideosSyncService } from '../../core/services/uploaded-videos-sync.service';
import { EditVideoFormDialog } from './edit-video-dialog/edit-video-form-dialog.component';
import { ConfirmationDialog } from '../confirmation-dialog.component';
import { Router } from '@angular/router';
import { ROUTES_CONFIG } from '../../core/routing-policy';


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
    private router: Router,
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
    const dialogRef = this.dialog.open(ConfirmationDialog, {
      autoFocus: false,
      height: 'auto',
      width: 'auto',
      maxWidth: 'calc(100% - 2rem)',
      data: {
        title: 'Are you sure you want to delete this video?'
      }
    });

    const sub = dialogRef.afterClosed().subscribe({
      next: (result: boolean) => {
        if (result) {
          this.deleteVideoRequest(video);
        }
      }
    });

    this.subscriptions.add(sub);
  }

  private deleteVideoRequest(video: UploadedVideo): void {
    const onSuccess = () => {
      this.userVideosList.removeVideo(video);
    }

    const onComplete = () => {
      video.sync = false;
    }

    video.sync = true;
    this.deleteVideo(video.hashId, onSuccess, onComplete);
  }

  private deleteVideo(hashId: string, onSuccess: Function, onComplete: Function): void {
    const sub = this.backendService.deleteVideo(hashId)
      .subscribe({
        next: onSuccess.bind(this),
        error: (error: Error) => {
          this.toast.error(error.message);
        },
        complete: onComplete.bind(this)
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
      exitAnimationDuration: '200ms'
    });
  }

  public onEditVideoRequest(video: UploadedVideo): void {
    this.openEditVideoFormDialog(video);
  }

  public openEditVideoFormDialog(video: UploadedVideo) {
    const dialogRef = this.dialog.open(EditVideoFormDialog, {
      autoFocus: false,
      height: 'auto',
      width: 'auto',
      maxWidth: 'calc(100% - 2rem)',
      exitAnimationDuration: '200ms',
      data: {
        video
      }
    })

    const sub = dialogRef.afterClosed().subscribe({
      next: (result: undefined | any) => {
        if (result === undefined) return;
        // update video on server
        this.updateVideo(video, result);
      },
      error: (error: Error) => {
        this.toast.error(error.message);
      }
    });

    this.subscriptions.add(sub);
  }

  private updateVideo(video: UploadedVideo, data: any): void {
    video.sync = true;
    const sub = this.backendService.updateVideo(video.hashId, data).subscribe({
      next: (respone: Object) => {
        // update video on client
        this.fetchUserVideosList();

        this.toast.success('Video updated successfully');
      },
      error: (error: Error) => {
        this.toast.error(error.message);
      },
      complete: () => {
        video.sync = false;
      }
    });

    this.subscriptions.add(sub);
  }

  public onWatchVideoRequest(video: UploadedVideo): void {
    this.router.navigate([
      `${ROUTES_CONFIG.WATCH.path}/${video.clientSideId()}`
    ]);
  }
}
