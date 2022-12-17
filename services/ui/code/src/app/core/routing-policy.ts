import { AuthGuard } from "./guards/auth-guard";
import { NegateAuthGuard } from "./guards/negate-auth-guard";
import { CanActivate } from "@angular/router";
import { _Constructor } from "@angular/material/core";
import { faCompass, faVideo, faLock, IconDefinition, faQuestion } from '@fortawesome/free-solid-svg-icons';

export const ROUTES_CONFIG: Readonly<{
    [key in routes_map]: RouteConfig
}> = Object.freeze({
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
    WATCH: {
        path: 'watch',
        title: 'Watch',
        canActivate: [],
        isAuthenticationNeeded: false,
        visibleToAuthenticatedUsers: true,
        navigationBarVisibility: false,
        children: {},
        icon: faQuestion
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
    }
});

export type RouteConfig = {
    path: string;
    title: string;
    canActivate: Array<_Constructor<CanActivate>>;
    isAuthenticationNeeded: boolean;
    visibleToAuthenticatedUsers: boolean;
    navigationBarVisibility: boolean;
    children: { [key: string]: RouteConfig };
    icon: IconDefinition;
}

type routes_map =
    'LOG_IN' |
    'WORKSPACE' |
    'WATCH' |
    'EXPLORE';
