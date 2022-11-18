import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HeaderModule } from './header/header.module';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { LogoModule } from './common/logo/logo.module';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { ContentModule } from './content/content.module';

import { ThemeService } from './core/services/theme.service';
import { BackendService } from './core/services/backend.service';
import { AuthService } from './core/services/auth.service';

import { AuthGuard } from './core/guards/auth-guard';
import { NegateAuthGuard } from './core/guards/negate-auth-guard';

import { AppComponent } from './app.component';


@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    FontAwesomeModule,
    HeaderModule,
    ContentModule,
    LogoModule,
    NgbModule,
    MatProgressBarModule
  ],
  providers: [
    ThemeService,
    BackendService,
    AuthService,
    AuthGuard,
    NegateAuthGuard
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
