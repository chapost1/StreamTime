import { Component, EventEmitter, Input, IterableDiffer, IterableDiffers, OnChanges, Output, SimpleChanges, ViewChild } from '@angular/core';
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
  @Output() editVideoEmitter: EventEmitter<Video> = new EventEmitter<Video>();
  @Output() deleteVideoEmitter: EventEmitter<Video> = new EventEmitter<Video>();
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

  private videosIterableDiffer: IterableDiffer<Video>;

  constructor(private iterableDiffers: IterableDiffers) {
    this.videosIterableDiffer = this.iterableDiffers.find(this.videos)
      .create(this.trackUnprocessedVideosChangesFn.bind(this));
  }

  ngDoCheck(): void {
    this.checkForUnprocessedVideosChange();
  }

  ngOnChanges(changes: SimpleChanges) {
    if ('videos' in changes) {
      this.onVideosChange();
    }
  }

  private checkForUnprocessedVideosChange(): void {
    const changes = this.videosIterableDiffer.diff(this.videos);
    if (changes) {
      this.onVideosChange();
    }
  }

  private onVideosChange(): void {
    this.dataSource.data = [...this.videos];
  }

  private trackUnprocessedVideosChangesFn(idx: number, video: Video): string {
    return video.hashId;
  }

  public displayedColumns(): string[] {
    return ['videoSummary', 'sizeInBytes', 'listingTime', 'isPrivate', 'uploadTimeTS'];
  }

  public onDelete(video: Video): void {
    this.deleteVideoEmitter.emit(video);
  }

  public onEdit(video: Video): void {
    this.editVideoEmitter.emit(video);
  }
}
