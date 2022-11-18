import { Observable, Subscription } from 'rxjs';

interface WrapperResponse {
    error: Error | null;
    data: any;
}
export const PromiseWrapper = (promise: Promise<unknown>): Promise<WrapperResponse> => {
    return new Promise(resolve => {
        promise
            .then(res => resolve({ error: null, data: res }))
            .catch(err => resolve({ error: err, data: null }));
    });
}

export const ObservableWrapper = (observable: Observable<unknown>): Promise<WrapperResponse> => {
    return new Promise(resolve => {
        let sub: null | Subscription = null;
        sub = observable.subscribe({
            next(data) {
                resolve({ error: null, data });
                unsubscribe();
            },
            error(error) {
                resolve({ error, data: null });
                unsubscribe();
            }
        });
        function unsubscribe() {
            setTimeout(() => (<Subscription>sub).unsubscribe(), 0);
        }
    });
}