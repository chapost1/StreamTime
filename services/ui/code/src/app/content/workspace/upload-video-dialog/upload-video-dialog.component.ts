import { Component, Inject, OnDestroy, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { faXmark, faCloudArrowUp } from '@fortawesome/free-solid-svg-icons';
import { Subscription } from 'rxjs';

@Component({
    selector: 'dialog-upload-video-dialog',
    templateUrl: 'upload-video-dialog.component.html'
})
export class UploadVideoDialog implements OnInit, OnDestroy {
    private subscriptions: Subscription = new Subscription();
    public faCloudArrowUp = faCloudArrowUp;
    public faXmark = faXmark;

    constructor(
        public dialogRef: MatDialogRef<UploadVideoDialog>,
        @Inject(MAT_DIALOG_DATA) public data: unknown,
    ) { }

    ngOnInit(): void {
        const keydownEvents = this.dialogRef.keydownEvents().subscribe(event => {
            if (event.key === "Escape") {
                this.exit();
            }
        });
        this.subscriptions.add(keydownEvents);
    }

    ngOnDestroy(): void {
        this.subscriptions.unsubscribe();
    }

    public exit(): void {
        this.dialogRef.close();
    }

    public selectFiles(): void {
        //todo: browse files
    }
}