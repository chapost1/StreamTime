from fastapi import APIRouter, Depends
from rds import videos
from uuid import UUID
from models import WatchVideoRecord
from ..auth_guards import any_user

router = APIRouter()

# watch a video
@router.get("/", response_model=WatchVideoRecord, response_model_exclude_none=True)
async def get_watch_video_record(user_id: UUID, hash_id: UUID, authenticated_user_id: str = Depends(any_user)) -> WatchVideoRecord:
    """todo: implement""" # if not private / private but user has premissions, create presigned url on S3
