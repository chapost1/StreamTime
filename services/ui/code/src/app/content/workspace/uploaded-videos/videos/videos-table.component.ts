import { Component, Input, OnChanges, SimpleChanges, ViewChild} from '@angular/core';
import Video from 'src/app/core/models/entities/videos/video';
import { faEye, faEyeSlash, faPenToSquare, faCheck } from '@fortawesome/free-solid-svg-icons';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';

@Component({
  selector: 'app-videos-table',
  templateUrl: 'videos-table.component.html',
  styleUrls: ['videos-table.component.scss']
})
export class VideosTableComponent implements OnChanges {
  @Input() videos: Video[] = [];
  @ViewChild(MatSort) set matSort(sort: MatSort) {
    this.dataSource.sort = sort;
  }
  public dataSource = new MatTableDataSource<Video>([]);

  public icons = {
    public: faEye,
    private: faEyeSlash,
    draft: faPenToSquare,
    listed: faCheck
  }

  ngOnChanges(changes: SimpleChanges) {
    if ('videos' in changes) {
      this.dataSource.data = [...(<Video[]>(changes['videos'].currentValue)) || []];
    }
  }

  public displayedColumns(): string[] {
    return ['videoSummary', 'sizeInBytes', 'listingTime', 'isPrivate', 'uploadTimeTS'];
  }
}
