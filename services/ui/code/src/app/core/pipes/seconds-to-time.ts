import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'secondsToTime' })
export class SecondsToTimePipe implements PipeTransform {
    transform(value: number): string {
        return this.secondsToHhMmSs(value);
    }

    private padTime(time: number): string {
        return time < 10 ? "0" + time : String(time);
    }

    private secondsToHhMmSs(durationSeconds: number): string {
        if (durationSeconds < 0) {
            return '00:00:00';
        }

        const hours = this.padTime(Math.floor(durationSeconds / 3600)),
            minutes = this.padTime(Math.floor((durationSeconds % 3600) / 60)),
            seconds = this.padTime(Math.floor(durationSeconds % 60));

        const time = [minutes, seconds];
        if (hours !== '00') {
            time.unshift(hours);
        }

        return time.join(':')
    };
}