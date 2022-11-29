import { Component, Input, OnChanges, SimpleChanges, ViewChild } from '@angular/core';
import UnprocessedVideo from 'src/app/core/models/entities/videos/unprocessed-video';
import { faTriangleExclamation, faTrashCan } from '@fortawesome/free-solid-svg-icons';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';

@Component({
  selector: 'app-unprocessed-videos-table',
  templateUrl: 'unprocessed-videos-table.component.html',
  styles: [
  ]
})
export class UnprocessedVideosTableComponent implements OnChanges {
  @Input() unprocessedVideos: UnprocessedVideo[] = [];
  @ViewChild(MatSort) set matSort(sort: MatSort) {
    this.dataSource.sort = sort;
  }
  public dataSource = new MatTableDataSource<UnprocessedVideo>([]);

  public icons = {
    error: faTriangleExclamation,
    delete: faTrashCan
  }

  ngOnChanges(changes: SimpleChanges) {
    if ('unprocessedVideos' in changes) {
      this.dataSource.data = [...(<UnprocessedVideo[]>(changes['unprocessedVideos'].currentValue)) || []];
    }
  }

  public displayedColumns(): string[] {
    return ['actions', 'failureReason', 'uploadTimeTS'];
  }
}
