import { Component, Inject, OnDestroy, OnInit, ViewChild, ElementRef } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { faXmark, faCloudArrowUp } from '@fortawesome/free-solid-svg-icons';
import { Subscription } from 'rxjs';
import { BackendService, VideoUploadConfig } from 'src/app/core/services/backend.service';
import { ObservableWrapper } from 'src/app/common/utils';
import { NgToastStackService } from 'ng-toast-stack';

@Component({
    selector: 'dialog-upload-video-dialog',
    templateUrl: './upload-video-dialog.component.html',
    styleUrls: ['./upload-video-dialog.component.scss']
})
export class UploadVideoDialog implements OnInit, OnDestroy {
    @ViewChild('fileUploadElement') fileUploadElement: ElementRef | undefined;

    private subscriptions: Subscription = new Subscription();

    private validFileTypes = new Set();

    private maxSizeInBytes = 0;

    public faCloudArrowUp = faCloudArrowUp;
    public faXmark = faXmark;

    public uploadConfigHasBeenRetrieved: boolean = false;
    public isUploadInProgress: boolean = false;

    constructor(
        public dialogRef: MatDialogRef<UploadVideoDialog>,
        @Inject(MAT_DIALOG_DATA) public data: unknown,
        private backendService: BackendService,
        private toast: NgToastStackService
    ) { }

    ngOnInit(): void {
        this.initUploadConfig();
        this.initListeners();
    }

    ngOnDestroy(): void {
        this.subscriptions.unsubscribe();
    }

    public exit(): void {
        this.dialogRef.close();
    }

    private initListeners(): void {
        const keydownEvents = this.dialogRef.keydownEvents().subscribe(event => {
            if (event.key === "Escape") {
                this.exit();
            }
        });
        this.subscriptions.add(keydownEvents);

        const backdropClick = this.dialogRef.backdropClick().subscribe(event => {
            this.exit();
        });
        this.subscriptions.add(backdropClick);
    }

    private async initUploadConfig(): Promise<void> {
        const sub = this.backendService.videoUploadConfig.subscribe({
            next: (config) => {
                if (!config) {
                    return;
                }
                this.validFileTypes = new Set((<VideoUploadConfig>config).valid_file_types || []);
                this.maxSizeInBytes = (<VideoUploadConfig>config).max_size_in_bytes;
                this.uploadConfigHasBeenRetrieved = true;
            },
            error: (err) => {
                console.error(err);
                this.toast.error('failed to retrieve video upload config');
                this.exit();
                return;
            }
        });
        this.subscriptions.add(sub);
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
            this.toast.error(errorMessage);
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
            const message = error.message || 'Could not upload the file!';
            this.toast.error(message);
        } else {
            this.toast.success('video has been uploaded');
        }

        this.isUploadInProgress = false;

        this.exit();
    }

}