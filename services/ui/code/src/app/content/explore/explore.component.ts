import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { NgToastStackService } from 'ng-toast-stack';
import { Subscription } from 'rxjs';
import VideosPage from '../../core/models/entities/videos/videos-page';
import Video from '../../core/models/entities/videos/video';
import { BackendService } from '../../core/services/backend.service';
import { faPlay } from '@fortawesome/free-solid-svg-icons';
import { Router } from '@angular/router';
import { ROUTES_CONFIG } from '../../core/routing-policy';
import TimeAgo from 'javascript-time-ago'
import en from 'javascript-time-ago/locale/en'
TimeAgo.addLocale(en)

@Component({
  selector: 'app-explore',
  templateUrl: './explore.component.html',
  styleUrls: ['./explore.component.scss']
})
export class ExploreComponent implements OnInit, OnDestroy {
  @ViewChild('scrollContainer') scrollContainer: any;

  private subscriptions: Subscription = new Subscription();
  private next: string | null = null;
  public hasNext: boolean = true;

  public videos: Video[] = [];

  public loadingMoreVideos: boolean = false;

  // pre-load 2 pages
  private loadMoreRequestsQueue: number = 2;

  public icons = {
    watch: faPlay
  }

  constructor(
    private router: Router,
    private backendService: BackendService,
    private toast: NgToastStackService
  ) { }

  ngOnInit(): void {
    this.loadMore();
  }

  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
  }

  public onScroll(): void {
    this.loadMoreRequestsQueue++;
    this.loadMore();
  }

  public loadMore(): void {
    if (this.loadMoreRequestsQueue <= 0) {
      return;
    }
    this.loadMoreRequestsQueue--;
    this.loadingMoreVideos = true;

    const sub = this.backendService.exploreVideos(this.next)
      .subscribe({
        next: (page: VideosPage) => {
          this.videos = this.videos.concat(page.videos);
          this.next = page.next;
          this.hasNext = page.hasNext()
          this.loadingMoreVideos = false;
        },
        error: (error) => {
          this.toast.error('Failed to load more videos');
          console.error(error);
          this.loadingMoreVideos = false;
        },
        complete: () => {
          if (0 < this.loadMoreRequestsQueue) {
            this.loadMore();
          }
        }
      })

    this.subscriptions.add(sub);
  }

  public timeAgo(date: string | null): string {
    const timeAgo = new TimeAgo('en-US');
    return timeAgo.format(new Date(<string>date));
  }

  public onWatch(video: Video): void {
    this.router.navigate([
      `${ROUTES_CONFIG.WATCH.path}/${video.clientSideId()}`
    ]);
  }
}
