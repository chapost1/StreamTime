import {
    Directive,
    Output,
    EventEmitter,
    HostBinding,
    HostListener
} from '@angular/core';

@Directive({
    selector: '[appDnd]'
})
export class DndDirective {
    @HostBinding('class.fileover') fileOver: boolean | undefined;
    @Output() fileDropped = new EventEmitter<any>();

    // Dragover listener
    @HostListener('dragover', ['$event']) onDragOver(event: DragEvent) {
        event.preventDefault();
        event.stopPropagation();
        this.fileOver = true;
    }

    // Dragleave listener
    @HostListener('dragleave', ['$event']) public onDragLeave(event: DragEvent) {
        event.preventDefault();
        event.stopPropagation();
        this.fileOver = false;
    }

    // Drop listener
    @HostListener('drop', ['$event']) public ondrop(event: DragEvent) {
        event.preventDefault();
        event.stopPropagation();
        this.fileOver = false;
        if (event.dataTransfer?.files) {
            const files = event.dataTransfer?.files;
            if (0 < files.length) {
                this.fileDropped.emit(files);
            }
        }
    }
}
