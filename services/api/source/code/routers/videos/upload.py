from typing import Dict
from fastapi import APIRouter, Depends
from ..auth_guards import authenticated_user

router = APIRouter()

# upload a video, cosider, maybe return a dataclass...
@router.get("/", response_model=Dict)
async def get_upload_video_url(authenticated_user_id: str = Depends(authenticated_user)) -> Dict:

    """todo: implement""" # create hash_id and presigned url on s3 (needs the bucket name)
