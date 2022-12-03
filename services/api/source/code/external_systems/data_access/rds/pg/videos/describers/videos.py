from __future__ import annotations
from external_systems.data_access.rds.pg.connection.connection import Connection
from external_systems.data_access.rds.abstract.videos import DescribedVideos
from external_systems.data_access.rds.pg.videos.describers.uploaded_videos import DescribedUploadedVideosPG
from typing import List, Tuple, Dict, Any
from entities.videos import Video
from entities.videos import VideoStages
from external_systems.data_access.rds.pg.videos import tables
from common.utils import nl
from uuid import UUID


class DescribedVideosPG(DescribedUploadedVideosPG):
    f"""
    Videos database class which implements the abstract protocol
    Uses postgres as a concrete implementation

    Abstract protocol docs:
    {DescribedVideos.__doc__}
    """

    excluded_user_id: UUID = None
    allowed_privates_of_user_id: UUID = None
    pagination_index_is_smaller_than: int = None
    unlisted_should_be_hidden: bool = False
    privates_should_be_hidden: bool = False
    requested_limit: int = None


    def build_query_conditions_params(self, base_conditions: List[str] = [], base_params: List[Any] = []) -> Tuple[List[str], List[Any]]:
        conditions, params = super().build_query_conditions_params(base_conditions=base_conditions, base_params=base_params)

        # hide anything which is related to the excluded user_id
        if self.excluded_user_id is not None:
            conditions.append('user_id::text != %s::text')
            params.append(self.excluded_user_id)


        # pagination index can appear also after user_id as it is an maintained index on pg side (user_id)
        if self.pagination_index_is_smaller_than is not None:
            conditions.append('pagination_index < %s')
            params.append(self.pagination_index_is_smaller_than)


        # assert query will return listed videos only
        if self.unlisted_should_be_hidden:
            conditions.append('listing_time is not null')


        # privates visibility control
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
            # do not allow privates by default
            conditions.append('is_private is not true')
        
        return conditions, params


    async def search(self) -> List[Video]:
        conditions, params = self.build_query_conditions_params()

        # keep limit as the last param
        # it is the last sql expression and it is also a condition by itself
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

        return list(map(self.__prase_db_records_into_classes, videos))
    

    async def delete(self) -> None:
        await super().delete(stage=VideoStages.READY.value)
    

    async def update(self, to_update: Dict) -> None:
        await super().update(to_update=to_update, stage=VideoStages.READY.value)


    def not_owned_by(self, user_id: UUID) -> DescribedVideosPG:
        self.excluded_user_id = user_id
        return self


    def include_privates_of(self, user_id: UUID) -> DescribedVideosPG:
        self.allowed_privates_of_user_id = user_id
        return self


    def filter_unlisted(self, flag: bool = True) -> DescribedVideosPG:
        self.unlisted_should_be_hidden = flag
        return self


    def filter_privates(self, flag: bool = True) -> DescribedVideosPG:
        self.privates_should_be_hidden = flag
        return self

    
    def paginate(self, pagination_index_is_smaller_than: int) -> DescribedVideosPG:
        self.pagination_index_is_smaller_than = pagination_index_is_smaller_than
        return self
    

    def limit(self, limit: int) -> DescribedVideosPG:
        self.requested_limit = limit
        return self


    def __prase_db_records_into_classes(self, video: Tuple) -> Video:
        return Video(
            hash_id=video[0],
            user_id=video[1],
            title=video[2],
            description=video[3],
            size_in_bytes=video[4],
            duration_seconds=video[5],
            video_type=video[6],
            thumbnail_url=video[7],
            _storage_object_key=video[8],
            _storage_thumbnail_key=video[9],
            upload_time=video[10],
            is_private=video[11],
            listing_time=video[12],
            pagination_index=video[13]
        )
