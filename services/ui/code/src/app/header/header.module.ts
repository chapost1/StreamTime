import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { RouterModule } from '@angular/router';

import { HeaderComponent } from './header.component';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { ThemeToggleComponent } from './toolbar/theme-toggle/theme-toggle.component';
import { LogoComponent } from '../common/logo/logo.component';


@NgModule({
  declarations: [
    LogoComponent,
    HeaderComponent,
    ToolbarComponent,
    ThemeToggleComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    FontAwesomeModule
  ],
  exports: [
    HeaderComponent
  ]
})
export class HeaderModule { }
