from entities.videos import Video


def prepare_listed_record_before_update(video: Video) -> Video:
    # omits fields which are immutable after listing
    record = video.dict(include=Video.ALLOWED_UPDATE_FIELDS_FOR_LISTED_VIDEOS)
    return Video(**record)
