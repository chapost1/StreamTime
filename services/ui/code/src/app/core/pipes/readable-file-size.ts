import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'readableFileSize' })
export class ReadableFileSizePipe implements PipeTransform {
    transform(value: number): string {
        return this.readableFileSize(value);
    }

    private readableFileSize(size: number): string {
        if (size < 0) {
            return '0 B';
        }
        const units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
        const fileFormatStepFactor = 1000;// on mem it's 1024
        let i = 0;
        while (size >= fileFormatStepFactor && i < units.length - 1) {
            size /= fileFormatStepFactor;
            i++;
        }
        return `${size.toFixed(1)} ${units[i]}`
    };
}