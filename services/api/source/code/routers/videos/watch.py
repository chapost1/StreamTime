from fastapi import APIRouter, Request
from rds import videos
from models import WatchVideoRecord

router = APIRouter()

# watch a video
@router.get("/", response_model=WatchVideoRecord, response_model_exclude_none=True)
async def get_watch_video_record(request: Request) -> WatchVideoRecord:
    """todo: implement""" # if not private / private but user has premissions, create presigned url on S3
