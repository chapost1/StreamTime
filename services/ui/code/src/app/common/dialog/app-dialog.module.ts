import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MatCardModule } from '@angular/material/card';

import { AppDialogComponent } from './dialog.component';


@NgModule({
    declarations: [
        AppDialogComponent
    ],
    imports: [
        CommonModule,
        MatCardModule
    ],
    exports: [
        AppDialogComponent
    ],
})
export class AppDialogModule { }
