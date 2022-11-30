import { Component, DoCheck, EventEmitter, Input, IterableDiffer, IterableDiffers, OnChanges, Output, SimpleChanges, ViewChild } from '@angular/core';
import UnprocessedVideo from 'src/app/core/models/entities/videos/unprocessed-video';
import { faTriangleExclamation, faTrashCan } from '@fortawesome/free-solid-svg-icons';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';

@Component({
  selector: 'app-unprocessed-videos-table',
  templateUrl: 'unprocessed-videos-table.component.html',
  styleUrls: ['unprocessed-videos-table.component.scss']
})
export class UnprocessedVideosTableComponent implements OnChanges, DoCheck {
  @Output() deleteVideoEmitter: EventEmitter<UnprocessedVideo> = new EventEmitter<UnprocessedVideo>();
  @Input() unprocessedVideos: UnprocessedVideo[] = [];
  @ViewChild(MatSort) set matSort(sort: MatSort) {
    this.dataSource.sort = sort;
  }
  public dataSource = new MatTableDataSource<UnprocessedVideo>([]);

  private unprocessedVideosIterableDiffer: IterableDiffer<UnprocessedVideo>;

  public icons = {
    error: faTriangleExclamation,
    delete: faTrashCan
  }

  constructor(private iterableDiffers: IterableDiffers) {
    this.unprocessedVideosIterableDiffer = this.iterableDiffers.find(this.unprocessedVideos)
      .create(this.trackUnprocessedVideosChangesFn.bind(this));
  }

  ngDoCheck(): void {
    this.checkForUnprocessedVideosChange();
  }

  ngOnChanges(changes: SimpleChanges) {
    if ('unprocessedVideos' in changes) {
      this.onUnprocessedVideosChange();
    }
  }

  private checkForUnprocessedVideosChange(): void {
    const changes = this.unprocessedVideosIterableDiffer.diff(this.unprocessedVideos);
    if (changes) {
      this.onUnprocessedVideosChange();
    }
  }

  private trackUnprocessedVideosChangesFn(idx: number, video: UnprocessedVideo): string {
    return video.hashId;
  }

  private onUnprocessedVideosChange(): void {
    this.dataSource.data = [...this.unprocessedVideos];
  }

  public displayedColumns(): string[] {
    return ['actions', 'failureReason', 'uploadTimeTS'];
  }

  public onDelete(video: UnprocessedVideo): void {
    this.deleteVideoEmitter.emit(video);
  }
}
