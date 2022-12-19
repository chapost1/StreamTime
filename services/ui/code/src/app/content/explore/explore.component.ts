import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import { NgToastStackService } from 'ng-toast-stack';
import { Subscription } from 'rxjs';
import VideosPage from '../../core/models/entities/videos/videos-page';
import Video from '../../core/models/entities/videos/video';
import { BackendService } from '../../core/services/backend.service';

@Component({
  selector: 'app-explore',
  templateUrl: './explore.component.html',
  styleUrls: ['./explore.component.scss']
})
export class ExploreComponent implements OnInit, OnDestroy {
  private subscriptions: Subscription = new Subscription();
  private next: string | null = null;
  public hasNext: boolean = true;

  public videos: Video[] = [];

  public loadMoreVideos: boolean = false;

  constructor(
    private backendService: BackendService,
    private toast: NgToastStackService
  ) { }

  ngOnInit(): void {
    this.loadMore();
  }

  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
  }

  // listen to scroll event
  // and load more videos if the user has scrolled to the bottom
  @HostListener('window:scroll', ['$event'])
  onScroll(event: any): void {
    if ((window.innerHeight + window.scrollY * 1.1) >= document.body.offsetHeight) {
      this.loadMore();
    }
  }

  public loadMore(): void {
    if (!this.hasNext || this.loadMoreVideos) {
      return;
    }

    this.loadMoreVideos = true;

    const sub = this.backendService.exploreVideos(this.next)
      .subscribe({
        next: (page: VideosPage) => {
          this.videos = this.videos.concat(page.videos);
          this.next = page.next;
          this.hasNext = page.hasNext()
        },
        error: (error) => {
          this.toast.error('Failed to load more videos');
          console.error(error);
        },
        complete: () => {
          this.loadMoreVideos = false;
        }
      })

    this.subscriptions.add(sub);
  }
}
