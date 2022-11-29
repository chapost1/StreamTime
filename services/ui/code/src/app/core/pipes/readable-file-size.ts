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
        var units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
        var i = 0;
        while(size >= 1024) {
            size /= 1024;
            ++i;
        }
        return `${size.toFixed(1)} ${units[i]}`
    };
}