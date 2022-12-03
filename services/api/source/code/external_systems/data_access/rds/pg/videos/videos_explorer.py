from __future__ import annotations
from external_systems.data_access.rds.pg.connection.connection import Connection
from external_systems.data_access.rds.abstract.videos.videos_explorer import VideosExplorer
from typing import List, Tuple, Callable
from entities.videos import Video
from external_systems.data_access.rds.pg.videos import tables
from common.utils import nl
from uuid import UUID


class VideosExplorerPG:
    f"""
    VideosExplorer database class which implements the abstract protocol
    Uses postgres as a concrete implementation

    Abstract protocol docs:
    {VideosExplorer.__doc__}
    """

    parse_function: Callable[[Tuple], Video]

    hash_id: UUID = None
    user_id: UUID = None
    excluded_user_id: UUID = None
    allowed_privates_of_user_id: UUID = None
    pagination_index_is_smaller_than: int = None
    unlisted_should_be_hidden: bool = False
    privates_should_be_hidden: bool = False
    requested_limit: int = None


    def __init__(self, parse_function: Callable[[Tuple], Video]) -> None:
        self.parse_function = parse_function


    async def search(self) -> List[Video]:
        conditions = []
        params = []

        if self.user_id is not None:
            # user_id is an index and therefore it is a good first filter condition
            conditions.append('user_id::text = %s::text')
            params.append(self.user_id)
        
        if self.hash_id is not None:
            conditions.append('hash_id::text = %s::text')
            params.append(self.hash_id)

        # pagination index can appear also after user_id as it is an maintained index on pg side (user_id)
        if self.pagination_index_is_smaller_than is not None:
            if self.pagination_index_is_smaller_than < 1:
                # pagination index range is [1, INT_MAX]
                # therefore, smaller than 1 means return nothing
                return []
            conditions.append('pagination_index < %s')
            params.append(self.pagination_index_is_smaller_than)
        
        if self.unlisted_should_be_hidden:
            # assert query will return listed videos only
            conditions.append('listing_time is not null')

        if self.privates_should_be_hidden:
            # force privates as hidden
            conditions.append('is_private is not true')
        elif self.allowed_privates_of_user_id is not None:
            # allow privates for specific user only
            # if this is not the allowed user, show only public (not private)
            # else, show for the auth user, anything
            conditions.append('((user_id::text != %s::text AND is_private is not true) OR (user_id::text = %s::text))')
            params.append(self.allowed_privates_of_user_id)
            params.append(self.allowed_privates_of_user_id)
        else:
            # do not allow privates at all
            conditions.append('is_private is not true')
        
        if self.excluded_user_id is not None:
            # hide anything which is related to the excluded user_id
            conditions.append('user_id::text != %s::text')
            params.append(self.excluded_user_id)    

        # keep limit as the last param, as it is the last sql expression
        params.append(self.requested_limit)
        
        videos = await Connection().query([
            (
                f"""SELECT 
                        hash_id,
                        user_id,
                        title,
                        description,
                        size_in_bytes,
                        duration_seconds,
                        video_type,
                        thumbnail_url,
                        storage_object_key,
                        storage_thumbnail_key,
                        upload_time,
                        is_private,
                        listing_time,
                        pagination_index
                FROM {tables.VIDEOS_TABLE}
                WHERE {f'{nl()}AND '.join(conditions)}
                ORDER BY pagination_index DESC
                LIMIT %s""",
                tuple(params)
            )
        ])

        return list(map(self.parse_function, videos))
    

    def id(self, id: UUID) -> VideosExplorer:
        self.hash_id = id
        return self


    def of_user(self, user_id: UUID) -> VideosExplorer:
        self.user_id = user_id
        return self
    

    def exclude_user(self, user_id: UUID) -> VideosExplorer:
        self.excluded_user_id = user_id
        return self


    def allow_privates_of(self, user_id: UUID) -> VideosExplorer:
        self.allowed_privates_of_user_id = user_id
        return self


    def paginate(self, pagination_index_is_smaller_than: int) -> VideosExplorer:
        self.pagination_index_is_smaller_than = pagination_index_is_smaller_than
        return self
    

    def limit(self, limit: int) -> VideosExplorer:
        self.requested_limit = limit
        return self


    def hide_unlisted(self, flag: bool = True) -> VideosExplorer:
        self.unlisted_should_be_hidden = flag
        return self


    def hide_privates(self, flag: bool = True) -> VideosExplorer:
        self.privates_should_be_hidden = flag
        return self
