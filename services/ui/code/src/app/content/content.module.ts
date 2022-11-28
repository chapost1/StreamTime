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

import { DndDirective } from '../core/directives/drag-and-drop.directive';

import { UploadVideoDialog } from './workspace/upload-video-dialog/upload-video-dialog.component';

import { LogoModule } from '../common/logo/logo.module';
import { ContentComponent } from './content.component';
import { WorkspaceComponent } from './workspace/workspace.component';
import { ExploreComponent } from './explore/explore.component';
import { LoginComponent } from './login/login.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { ContentPaddingComponent } from '../common/content/content-padding.component';
import { UploadedVideosComponent } from './workspace/uploaded-videos/uploaded-videos.component';


@NgModule({
  declarations: [
    ContentComponent,
    WorkspaceComponent,
    ExploreComponent,
    LoginComponent,
    PageNotFoundComponent,
    ContentPaddingComponent,
    UploadVideoDialog,
    DndDirective,
    UploadedVideosComponent
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
    MatProgressSpinnerModule
  ],
  exports: [
    ContentComponent,
  ],
  bootstrap: [ContentComponent],
  entryComponents: [UploadVideoDialog]
})
export class ContentModule { }
