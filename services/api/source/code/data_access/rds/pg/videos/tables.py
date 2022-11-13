from models.videos import VideoStages

VIDEOS_TABLE = 'videos'
UNPROCESSED_VIDEOS_TABLE = 'unprocessed_videos'

def video_stages_to_table(stage: VideoStages):
    if stage == VideoStages.UNPROCESSED.value:
        return UNPROCESSED_VIDEOS_TABLE
    elif stage == VideoStages.READY.value:
        return VIDEOS_TABLE

    return None
