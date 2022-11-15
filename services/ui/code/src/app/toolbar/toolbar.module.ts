import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import {RouterModule} from '@angular/router';

import { ToolbarComponent } from './toolbar.component';
import { ThemeToggleComponent } from './theme-toggle/theme-toggle.component';
import { LogoComponent } from '../common/logo/logo.component';


@NgModule({
  declarations: [
    LogoComponent,
    ToolbarComponent,
    ThemeToggleComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    MatToolbarModule,
    MatSlideToggleModule,
    FontAwesomeModule
  ],
  exports: [
    ToolbarComponent
  ]
})
export class ToolbarModule { }
