import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

import { ToolbarComponent } from './toolbar.component';


@NgModule({
  declarations: [
    ToolbarComponent
  ],
  imports: [
    CommonModule,
    MatToolbarModule,
    MatSlideToggleModule,
    FontAwesomeModule
  ],
  exports: [
    ToolbarComponent
  ]
})
export class ToolbarModule { }
