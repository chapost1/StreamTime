import { Component, Inject, OnInit, OnDestroy } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { NgToastStackService } from 'ng-toast-stack';
import Video from 'src/app/core/models/entities/videos/video';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Subscription } from 'rxjs';

export interface EditVideoDialogData {
    video: Video;
}

@Component({
    selector: 'dialog-edit-video-form-dialog',
    templateUrl: './edit-video-form-dialog.component.html',
    styleUrls: ['./edit-video-form-dialog.component.scss']
})
export class EditVideoFormDialog implements OnInit, OnDestroy {
    private subscriptions: Subscription = new Subscription();

    public saveButtonText: string = 'Publish';

    // TODO: Add thumbnail support

    public editables = new FormGroup({
        title: new FormControl('', [
            Validators.required,
            Validators.minLength(2)
        ]),
        description: new FormControl(''),
        isPrivate: new FormControl(false)
    });

    constructor(
        public dialogRef: MatDialogRef<EditVideoFormDialog>,
        @Inject(MAT_DIALOG_DATA) public data: EditVideoDialogData,
        private toast: NgToastStackService
    ) { }

    ngOnInit(): void {
        this.initListeners();
        
        this.setupLayout();

        this.syncFormWithVideo();
    }

    ngOnDestroy(): void {
        this.subscriptions.unsubscribe();
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

    public exit(result: undefined | any = undefined): void {
        this.dialogRef.close(result);
    }

    private setupLayout(): void {
        this.saveButtonText = 'Publish';
        if (this.data.video.isListed()) {
            this.saveButtonText = 'Save';
        }
    }

    private syncFormWithVideo(): void {
        let title = null;
        // force title to be null if video is not listed
        // so user would have to enter a new title
        if (this.data.video.isListed()) {
            title = this.data.video.title;
        }

        this.editables.controls.title.setValue(title);
        this.editables.controls.description.setValue(this.data.video.description);
        this.editables.controls.isPrivate.setValue(this.data.video.isPrivate);
    }

    public get isDeltaFound(): boolean {
        const title = this.editables.controls.title.value;
        const description = this.editables.controls.description.value;
        const isPrivate = this.editables.controls.isPrivate.value;
        
        if (title && title !== this.data.video.title) {
            return true;
        }

        if (description && description !== this.data.video.description) {
            return true;
        }

        if (isPrivate !== this.data.video.isPrivate) {
            return true;
        }

        return false;
    }

    public onFormSubmit(): void {
        if (this.editables.invalid) {
            this.toast.error('Please fix the errors in the form');
            return;
        }

        const payload = {
            title: this.editables.controls.title.value,
            description: this.editables.controls.description.value || '',
            isPrivate: this.editables.controls.isPrivate.value,
        };

        this.exit(payload);
    }
}
