import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { RouterModule } from '@angular/router';
import { LogoModule } from '../common/logo/logo.module';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatButtonModule } from '@angular/material/button';

import { HeaderComponent } from './header.component';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { ThemeToggleComponent } from './toolbar/theme-toggle/theme-toggle.component';


@NgModule({
  declarations: [
    HeaderComponent,
    ToolbarComponent,
    ThemeToggleComponent
  ],
  imports: [
    CommonModule,
    MatButtonModule,
    LogoModule,
    RouterModule,
    FontAwesomeModule,
    MatTooltipModule
  ],
  exports: [
    HeaderComponent
  ]
})
export class HeaderModule { }
