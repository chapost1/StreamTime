import { AuthGuard } from "../core/guards/auth-guard";
import { NegateAuthGuard } from "../core/guards/negate-auth-guard";
import { CanActivate } from "@angular/router";
import { _Constructor } from "@angular/material/core";
import { faCompass, faVideo, faLock, faQuestion, IconDefinition } from '@fortawesome/free-solid-svg-icons';



export interface RouteConfig {
    path: string;
    title: string;
    canActivate: Array<_Constructor<CanActivate>>;
    isAuthenticationNeeded: boolean;
    visibleToAuthenticatedUsers: boolean;
    navigationBarVisibility: boolean;
    children: { [key: string]: RouteConfig };
    icon: IconDefinition;
}
export const ROUTES_CONFIG = Object.freeze({
    LOG_IN: {
        path: 'login',
        title: 'Login',
        canActivate: [NegateAuthGuard],
        isAuthenticationNeeded: false,
        visibleToAuthenticatedUsers: false,
        navigationBarVisibility: true, 
        children: {},
        icon: faLock
    },
    WORKSPACE: {
        path: 'workspace',
        title: 'Workspace',
        canActivate: [AuthGuard],
        isAuthenticationNeeded: true,
        visibleToAuthenticatedUsers: true,
        navigationBarVisibility: true,
        children: {},
        icon: faVideo
    },
    EXPLORE: {
        path: 'explore',
        title: 'Explore',
        canActivate: [],
        isAuthenticationNeeded: false,
        visibleToAuthenticatedUsers: true,
        navigationBarVisibility: true,
        children: {},
        icon: faCompass
    },
    PAGE_NOT_FOUND: {
        path: '404',
        title: 'Page Not Found',
        canActivate: [],
        isAuthenticationNeeded: false,
        visibleToAuthenticatedUsers: true,
        navigationBarVisibility: false,
        children: {},
        icon: faQuestion
    }
});
