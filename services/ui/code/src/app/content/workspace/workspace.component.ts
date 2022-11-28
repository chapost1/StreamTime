import { Component, OnDestroy, OnInit } from '@angular/core';
import { faSquarePlus } from '@fortawesome/free-solid-svg-icons';
import { MatDialog } from '@angular/material/dialog';
import { UploadVideoDialog } from './upload-video-dialog/upload-video-dialog.component';
import { Subscription } from 'rxjs';
import { userVideosList as userVideosListMock } from './mocks';

@Component({
  selector: 'app-workspace',
  templateUrl: './workspace.component.html',
  styleUrls: ['./workspace.component.scss']
})
export class WorkspaceComponent implements OnInit, OnDestroy {
  private subscriptions: Subscription = new Subscription();
  public faSquarePlus = faSquarePlus;

  public userVideosListMock = userVideosListMock;

  constructor(public dialog: MatDialog) { }

  ngOnInit(): void {
    // todo:
    // open WS connection

    // todo: retrieve list of authenticated user video assets & pass it to some view oriented child componenet
  }

  ngOnDestroy(): void {
    // todo:
    // close WS connection

    this.subscriptions.unsubscribe();
  }

  openUploadVideoDialog() {
    this.dialog.open(UploadVideoDialog, {
      autoFocus: false,
      height: 'auto',
      minWidth: 'calc(100% - 2rem)',
      disableClose: true,
      exitAnimationDuration: '200ms'
    });
  }
}
