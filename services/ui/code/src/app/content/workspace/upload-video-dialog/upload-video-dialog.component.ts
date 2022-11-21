import { HttpResponse, HttpEventType } from '@angular/common/http';
import { Component, Inject, OnDestroy, OnInit, ViewChild, ElementRef } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { faXmark, faCloudArrowUp } from '@fortawesome/free-solid-svg-icons';
import { Subscription, Observable } from 'rxjs';
import { BackendService } from 'src/app/core/services/backend.service';
import { ObservableWrapper, PromiseWrapper } from 'src/app/common/utils';

@Component({
    selector: 'dialog-upload-video-dialog',
    templateUrl: 'upload-video-dialog.component.html',
    styleUrls: ['upload-video-dialog.component.scss']
})
export class UploadVideoDialog implements OnInit, OnDestroy {
    @ViewChild('fileUploadElement') fileUploadElement: ElementRef | undefined;

    private subscriptions: Subscription = new Subscription();
    public faCloudArrowUp = faCloudArrowUp;
    public faXmark = faXmark;

    private validFileTypes = new Set(
        [
            'video/ogg',
            'video/mp4',
            'video/webm',
            'video/mpeg'
        ]
    );

    private maxSizeInBytes = 2e+9;// todo: use dynamic config var

    public isUploadInProgress: boolean = false;

    constructor(
        public dialogRef: MatDialogRef<UploadVideoDialog>,
        @Inject(MAT_DIALOG_DATA) public data: unknown,
        private backendService: BackendService
    ) {
        this.fileUploadElement
    }

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

    public openFileSelectionBrowser(): void {
        if (this.isUploadInProgress) {
            return;
        }
        this.fileUploadElement?.nativeElement.click();
    }

    public onFileSelection(event: any): void {
        const element = event.target;
        const file: File | null = this.popSelectedFileFromElement(element);
        if (!file) {
            return;
        }

        const errorMessage = this.validateFile(file);
        if (errorMessage) {
            alert(errorMessage); // todo: snackbar
            return;
        }

        this.upload(file);
    }

    private popSelectedFileFromElement(element: HTMLInputElement): File | null {
        if (element.files) {
            const file: File | null = element.files?.item(0);
            this.resetFileUploadElement(element);
            return file;
        }
        return null;
    }

    private resetFileUploadElement(element: HTMLInputElement): void {
        element.value = '';
    }

    private validateFile(file: File): string | null {
        // type
        const type = file.type;
        if (!this.validFileTypes.has(type)) {
            return `${type} file type is unsupported. try one of these: ${Array.from(this.validFileTypes).join(', ')}`;
        }
        // size
        const sizeInBytes = file.size;
        if (this.maxSizeInBytes < sizeInBytes) {
            return `maximum file size exceeded by ${file.size / this.maxSizeInBytes * 100}%. maximum size is: ${this.maxSizeInBytes * (1e-9)}GB`;
        }

        return null;
    }

    private async upload(file: File): Promise<void> {
        this.isUploadInProgress = true;

        const { error } = await ObservableWrapper(
            this.backendService.uploadVideoFile(file)
        )
        if (error) {
            if (error.message) {
                const message = error.message;
                alert(message);// todo: snackbar
            } else {
                const message = 'Could not upload the file!';
                alert(message);// todo: snackbar
            }
        }

        this.isUploadInProgress = false;
        // display happy sucessfull snackbar

        this.exit();
    }

}