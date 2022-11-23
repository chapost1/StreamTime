import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ROUTES_CONFIG } from '../common/routing-policy';
import { WorkspaceComponent } from './workspace/workspace.component';
import { ExploreComponent } from './explore/explore.component';
import { LoginComponent } from './login/login.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

const routes: Routes = [
  { path: '', redirectTo: ROUTES_CONFIG.EXPLORE.path, pathMatch: 'full' },
  { path: ROUTES_CONFIG.WORKSPACE.path, component: WorkspaceComponent, canActivate: ROUTES_CONFIG.WORKSPACE.canActivate },
  { path: ROUTES_CONFIG.EXPLORE.path, component: ExploreComponent, canActivate: ROUTES_CONFIG.EXPLORE.canActivate },
  { path: ROUTES_CONFIG.LOG_IN.path, component: LoginComponent, canActivate: ROUTES_CONFIG.LOG_IN.canActivate },
  { path: '**', pathMatch: 'full', component: PageNotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ContentRoutingModule { }
