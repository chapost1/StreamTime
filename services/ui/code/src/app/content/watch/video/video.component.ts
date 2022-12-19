import { Component, ElementRef, Input, OnDestroy, SimpleChanges, ViewChild, ViewEncapsulation } from '@angular/core';
import WatchVideoRecord from '../../../core/models/entities/videos/watch-video-record';
import videojs from 'video.js';


@Component({
  selector: 'app-watch-video',
  templateUrl: './video.component.html',
  styleUrls: ['./video.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class WatchVideoComponent implements OnDestroy {

  @ViewChild('player', { static: true }) target: ElementRef | undefined;

  @ViewChild('description') description: ElementRef | undefined;

  @Input() public watchVideoRecord: WatchVideoRecord | undefined;

  private player: videojs.Player | undefined;

  public minimizeDescription: boolean = true;

  ngOnChanges(changes: SimpleChanges) {
    if ('watchVideoRecord' in changes && changes['watchVideoRecord'].currentValue) {
      this.initPlayer(changes['watchVideoRecord'].currentValue);
    }
  }

  ngOnDestroy() {
    if (this.player) {
      this.player.dispose();
    }
  }

  private initPlayer(watchVideoRecord: WatchVideoRecord): void {
    // instantiate Video.js
    this.player = this.play(
      this.buildPlayerOptions(watchVideoRecord)
    );

    this.player?.on('error', (err) => {
      // todo: handle the case when the video access time is expired
      console.log('error', err);
    });
  }

  private buildPlayerOptions(watchVideoRecord: WatchVideoRecord): videojs.PlayerOptions {
    const options: videojs.PlayerOptions = {
      preload: 'auto',
      bigPlayButton: true,
      playbackRates: [0.5, 1, 1.5, 2],
      aspectRatio: '16:9',
      fill: true,
      playsinline: true,
      controls: true,
      controlBar: {
        'liveDisplay': true,
        'pictureInPictureToggle': false
      },
      sources: [
        {
          src: watchVideoRecord.watchableUrl,
          type: watchVideoRecord.video.videoType
        }
      ]
    };

    return options;
  }

  private play(options: videojs.PlayerOptions): videojs.Player {
    return videojs(this.target?.nativeElement, options);
  }

  public toggleDescriptionVisibility(): void {
    this.minimizeDescription = !this.minimizeDescription;
  }

  public isDescriptionTextClipped(): boolean {
    const el = this.description?.nativeElement;
    if (!el) {
      // element is still undefined
      // default is false, so the toggle button will not be shown
      return false;
    }
    return el.scrollHeight > el.clientHeight;
  }
}
