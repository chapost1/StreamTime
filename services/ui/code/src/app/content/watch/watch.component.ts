import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NgToastStackService } from 'ng-toast-stack';
import UploadedVideo from '../../core/models/entities/videos/uploaded-video';
import { IUserIdHashId } from '../../core/models/entities/videos/uploaded-video';
import { BackendService } from '../../core/services/backend.service';
import { Subscription } from 'rxjs';
import WatchVideoRecord from '../../core/models/entities/videos/watch-video-record';

@Component({
  selector: 'app-watch',
  templateUrl: './watch.component.html',
  styles: []
})
export class WatchComponent implements OnInit, OnDestroy {
  private subscriptions: Subscription = new Subscription();

  public fetchWatchableRecord: boolean = false;

  public watchVideoRecord: WatchVideoRecord | undefined;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private backendService: BackendService,
    private toast: NgToastStackService
  ) { }

  ngOnInit(): void {
    this.prepareVideo();
  }

  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
  }

  private detectVideoIdentifiers(): IUserIdHashId | null {
    const videoClientSideId = this.route.snapshot.paramMap.get('id');
    if (videoClientSideId === null) {
      return null;
    }
    try {
      return UploadedVideo.clientSideIdToUserIdHashId(videoClientSideId);
    } catch (error) {
      return null;
    }
  }

  private invalidWatchRequest(): void {
    this.toast.error('Invalid watch request');
    this.backToHome();
  }

  private backToHome(): void {
    this.router.navigate(['/']);
  }

  private prepareVideo(): void {
    const videoIdentifiers = this.detectVideoIdentifiers();
    if (videoIdentifiers === null) {
      this.invalidWatchRequest();
      return;
    }

    this.fetchWatchableRecord = true;

    const sub = this.backendService
      .getWatchVideoRecord(videoIdentifiers)
      .subscribe({
        next: (record: WatchVideoRecord) => {
          this.watchVideoRecord = record;
        },
        error: (error) => {
          this.toast.error(error.message);
          this.backToHome();
        },
        complete: () => {
          this.fetchWatchableRecord = false;
        }
      })

    this.subscriptions.add(sub);
  }

}
