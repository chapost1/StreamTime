import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ContentRoutingModule } from './content-routing.module';

import { ContentComponent } from './content.component';
import { WorkspaceComponent } from './workspace/workspace.component';
import { ExploreComponent } from './explore/explore.component';
import { LoginComponent } from './login/login.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';


@NgModule({
  declarations: [
    ContentComponent,
    WorkspaceComponent,
    ExploreComponent,
    LoginComponent,
    PageNotFoundComponent
  ],
  imports: [
    CommonModule,
    ContentRoutingModule
  ],
  exports: [
    ContentComponent,
  ],
  bootstrap: [ContentComponent]
})
export class ContentModule { }
