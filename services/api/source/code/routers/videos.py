from typing import List
from fastapi import APIRouter, Request
from rds import videos
from models import Video

router = APIRouter(tags=["Video"])

# list all videos which are already listed
@router.get("/", response_model=List[Video])
async def get_listed_videos(request: Request) -> List[Video]:
    return await videos.get_listed_videos()

# todo implement:

# request upload video premission (will return presigned url) (will require nothing)

# list user videos (include tables: unprocessed, drafts, && and fields: is listed , is private)

# put video (using the hash_id of one which is not listed (check it out) && user_id(is already known))

# delete video / unprocessed video (will be known because of user_id/hash_id combo)
