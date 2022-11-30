import { Component, OnDestroy, OnInit } from '@angular/core';
import { faSquarePlus } from '@fortawesome/free-solid-svg-icons';
import { MatDialog } from '@angular/material/dialog';
import { UploadVideoDialog } from './upload-video-dialog/upload-video-dialog.component';
import { Subscription } from 'rxjs';
import { BackendService } from 'src/app/core/services/backend.service';
import { NgToastStackService } from 'ng-toast-stack';
import { UserVideosList } from 'src/app/core/models/entities/videos/types';

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
            resolve();
          },
          error: (e) => {
            this.toast.error(e);
            resolve();
          }
        });

      this.subscriptions.add(sub);
    })
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
