from fastapi import APIRouter, Request
from rds import videos
from uuid import UUID
from models import WatchVideoRecord

router = APIRouter()

# watch a video
@router.get("/", response_model=WatchVideoRecord, response_model_exclude_none=True)
async def get_watch_video_record(request: Request, user_id: UUID, hash_id: UUID) -> WatchVideoRecord:
    """todo: implement""" # if not private / private but user has premissions, create presigned url on S3
