function assertField(origin: string, name: string, value: any): void {
    origin = origin || 'anonymous';
    if (typeof value === 'undefined' || value === null) {
        const diagnose = `missing required field ${name}`;
        throw new Error(`${origin}: ${diagnose}`);        
    }
}

export default assertField;