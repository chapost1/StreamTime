import { Component, Inject, OnDestroy, OnInit, ViewChild, ElementRef } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { faXmark, faCloudArrowUp } from '@fortawesome/free-solid-svg-icons';
import { Subscription } from 'rxjs';
import { IUploadResponse } from '../../../core/models/backend/upload.types';
import { BackendService } from '../../../core/services/backend.service';
import { HttpResponse, HttpEventType } from '@angular/common/http';
import { NgToastStackService } from 'ng-toast-stack';
import UploadConfig from '../../../core/models/entities/upload-config';
import { ReadableFileSizePipe } from '../../../core/pipes/readable-file-size';

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

    public icons = {
        uploadAreaIcon: faCloudArrowUp,
        exitBtn: faXmark
    }

    public uploadConfigHasBeenRetrieved: boolean = false;
    public isUploadInProgress: boolean = false;
    public uploadProgress: number = 0;

    constructor(
        public dialogRef: MatDialogRef<UploadVideoDialog>,
        @Inject(MAT_DIALOG_DATA) public data: unknown,
        private backendService: BackendService,
        private toast: NgToastStackService,
        private readableFileSizePipe: ReadableFileSizePipe
    ) { }

    ngOnInit(): void {
        this.initUploadConfig();
    }

    ngOnDestroy(): void {
        this.subscriptions.unsubscribe();
    }

    public exit(): void {
        this.dialogRef.close();
    }

    private async initUploadConfig(): Promise<void> {
        const sub = this.backendService.videoUploadConfig.subscribe({
            next: (config: UploadConfig | undefined) => {
                if (!(config instanceof UploadConfig)) {
                    return;
                }
                
                this.validFileTypes = new Set(config.validFileTypes);
                this.maxSizeInBytes = config.maxSizeInBytes;
                this.uploadConfigHasBeenRetrieved = true;
            },
            error: (err: Error) => {
                console.error(err);
                this.toast.error('failed to retrieve video upload config');
                this.exit();
            }
        });
        this.subscriptions.add(sub);
    }

    public onFileDropped(files: FileList): void {
        if (this.isUploadInProgress) {
            return;
        }
        const file: File | null = this.extractFileFromList(files);
        if (!file) {
            return;
        }

        this.newFileHandler(file);
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
        this.newFileHandler(file);
    }

    private newFileHandler(file: File) {
        const errorMessage = this.validateFile(file);
        if (errorMessage) {
            this.toast.error(errorMessage);
            return;
        }

        this.upload(file);
    }

    private popSelectedFileFromElement(element: HTMLInputElement): File | null {
        if (element.files) {
            const file: File | null = this.extractFileFromList(element.files);
            this.resetFileUploadElement(element);
            return file;
        }
        return null;
    }

    private extractFileFromList(files: FileList): File | null {
        const file: File | null = files?.item(0);
        return file;
    }

    private resetFileUploadElement(element: HTMLInputElement): void {
        element.value = '';
    }

    private validateFile(file: File): string | null {
        // type
        const type = file.type;
        if (!this.validFileTypes.has(type)) {
            return `${type} file type is unsupported. try one of: ${Array.from(this.validFileTypes).join(', ')}.`;
        }
        // size
        const sizeInBytes = file.size;
        if (this.maxSizeInBytes < sizeInBytes) {
            const readableMaxSize = this.readableFileSizePipe.transform(this.maxSizeInBytes);
            const exceededBy = sizeInBytes / this.maxSizeInBytes * 100;
            return `maximum file size exceeded by ${exceededBy}%. maximum size is: ${readableMaxSize}`;
        }

        return null;
    }

    private async upload(file: File): Promise<void> {
        this.isUploadInProgress = true;

        const done = () => {
            this.isUploadInProgress = false;
            this.uploadProgress = 0;
            this.exit();
        }

        this.subscriptions.add(
            this.backendService.uploadVideoFile(file).subscribe({
                next: (event: IUploadResponse) => {
                    if (event && event.type === HttpEventType.UploadProgress) {
                        this.uploadProgress = Math.round(100 * event.loaded / event.total);
                    } else if (event instanceof HttpResponse) {
                        this.toast.success('video has been uploaded');
                        done();
                    }
                },
                error: (error: Error) => {
                    const message = error.message || 'Could not upload the file!';
                    this.toast.error(message);
                    done();
                }
            })
        );
    }
}
