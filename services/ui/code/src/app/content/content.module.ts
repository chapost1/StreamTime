import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AppDialogModule } from '../common/dialog/app-dialog.module';

import { ContentRoutingModule } from './content-routing.module';
import { MatToolbarModule } from '@angular/material/toolbar';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome'
import { MatButtonModule } from '@angular/material/button';;
import { MatDialogModule } from '@angular/material/dialog';
import { MatCardModule } from '@angular/material/card';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTableModule } from '@angular/material/table';
import { MatSortModule } from '@angular/material/sort';
import { MatInputModule } from '@angular/material/input';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { DndDirective } from '../core/directives/drag-and-drop.directive';

import { ConfirmationDialog } from './confirmation-dialog.component';
import { UploadVideoDialog } from './workspace/upload-video-dialog/upload-video-dialog.component';
import { EditVideoFormDialog } from './workspace/edit-video-dialog/edit-video-form-dialog.component';

import { LogoModule } from '../common/logo/logo.module';
import { ContentComponent } from './content.component';
import { WorkspaceComponent } from './workspace/workspace.component';
import { ExploreComponent } from './explore/explore.component';
import { LoginComponent } from './login/login.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { ContentPaddingComponent } from '../common/content/content-padding.component';
import { UploadedVideosComponent } from './workspace/uploaded-videos/uploaded-videos.component';
import { VideoSummaryComponent } from './workspace/uploaded-videos/videos/video-summary/video-summary.component';
import { VideosTableComponent } from './workspace/uploaded-videos/videos/videos-table.component';
import { UnprocessedVideosTableComponent } from './workspace/uploaded-videos/unprocessed-videos/unprocessed-videos-table.component';

import { SecondsToTimePipe } from '../core/pipes/seconds-to-time';
import { ReadableFileSizePipe } from '../core/pipes/readable-file-size';


@NgModule({
  declarations: [
    SecondsToTimePipe,
    ReadableFileSizePipe,
    ContentComponent,
    WorkspaceComponent,
    ExploreComponent,
    LoginComponent,
    PageNotFoundComponent,
    ContentPaddingComponent,
    UploadVideoDialog,
    DndDirective,
    UploadedVideosComponent,
    VideoSummaryComponent,
    VideosTableComponent,
    UnprocessedVideosTableComponent,
    EditVideoFormDialog,
    ConfirmationDialog
  ],
  imports: [
    LogoModule,
    CommonModule,
    AppDialogModule,
    ContentRoutingModule,
    MatToolbarModule,
    FontAwesomeModule,
    MatButtonModule,
    MatDialogModule,
    MatCardModule,
    MatTooltipModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatTableModule,
    MatSortModule,
    MatInputModule,
    FormsModule,
    ReactiveFormsModule,
    MatCheckboxModule
  ],
  exports: [
    ContentComponent,
  ],
  providers: [
    ReadableFileSizePipe
  ],
  bootstrap: [ContentComponent],
  entryComponents: [
    UploadVideoDialog,
    EditVideoFormDialog,
    ConfirmationDialog
  ]
})
export class ContentModule { }
