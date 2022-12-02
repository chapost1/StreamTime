from entities.videos import VideoStages

# supported videos tables
VIDEOS_TABLE = 'videos'
UNPROCESSED_VIDEOS_TABLE = 'unprocessed_videos'


def video_stages_to_table(stage: VideoStages) -> str:
    """Translates VideoStage enum to appropriate table"""

    if stage == VideoStages.UNPROCESSED.value:
        return UNPROCESSED_VIDEOS_TABLE
    elif stage == VideoStages.READY.value:
        return VIDEOS_TABLE

    return None
