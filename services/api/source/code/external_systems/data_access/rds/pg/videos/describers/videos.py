from __future__ import annotations
from external_systems.data_access.rds.pg.videos.describers.uploaded_videos import UploadedVideosDescriberPG
from typing import List, Tuple, Dict, Any
from entities.videos import Video
from entities.videos import VideoStages
from external_systems.data_access.rds.pg.videos import tables
from common.utils import nl
from uuid import UUID


class VideosDescriberPG(UploadedVideosDescriberPG):
    f"""
    VideosDescriber database class
    Uses postgres as a concrete implementation
    """

    excluded_user_ids: List[UUID]
    allowed_privates_of_user_ids: List[UUID]
    pagination_index_is_smaller_than: int
    unlisted_should_be_hidden: bool
    allow_privates_globally: bool
    requested_limit: int


    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.excluded_user_ids = []
        self.allowed_privates_of_user_ids = []
        self.pagination_index_is_smaller_than = None
        self.unlisted_should_be_hidden = False
        self.allow_privates_globally = False
        self.requested_limit = None


    def build_query_conditions_params(self, conditions: List[str] = [], params: List[Any] = []) -> Tuple[List[str], List[Any]]:
        conditions, params = super().build_query_conditions_params(conditions=conditions, params=params)

        # ignore anything which is related to the excluded user ids
        conditions, params = self.build_excluded_user_ids_conditions_params(conditions=conditions, params=params)

        # pagination index can appear also after user_id as it is an maintained index on pg side (user_id)
        conditions, params = self.build_pagination_conditions_params(conditions=conditions, params=params)

        # assert query will return listed videos only
        conditions, params = self.build_listing_conditions_params(conditions=conditions, params=params)

        # privates visibility control
        conditions, params = self.build_privacy_conditions_params(conditions=conditions, params=params)

        return conditions, params


    def build_excluded_user_ids_conditions_params(self, conditions: List[str] = [], params: List[Any] = []) -> Tuple[List[str], List[Any]]:
        return super().build_property_conditions_params(
            raw_params=self.excluded_user_ids,
            col_name='user_id',
            exclude=True,
            conditions=conditions,
            params=params
        )


    def build_pagination_conditions_params(self, conditions: List[str] = [], params: List[Any] = []) -> Tuple[List[str], List[Any]]:
        conditions = conditions.copy()
        params = params.copy()
        if self.pagination_index_is_smaller_than is not None:
            conditions.append('pagination_index < %s')
            params.append(self.pagination_index_is_smaller_than)
        return conditions, params
    

    def build_listing_conditions_params(self, conditions: List[str] = [], params: List[Any] = []) -> Tuple[List[str], List[Any]]:
        conditions = conditions.copy()
        if self.unlisted_should_be_hidden:
            conditions.append('listing_time is not null')
        return conditions, params


    def build_privacy_conditions_params(self, conditions: List[str] = [], params: List[Any] = []) -> Tuple[List[str], List[Any]]:
        # by default privates are disabled
        if self.allow_privates_globally:
            ...
        elif 0 < len(self.allowed_privates_of_user_ids):
            # allow privates for specified users
            conditions = conditions.copy()
            params = params.copy()

            s = []
            for param in self.allowed_privates_of_user_ids:
                s.append(self.cast(val_name='%s', casting_type='text'))
                params.append(param)

            # need to be strict regarding whether it is an allowed user or it should be determined by privacy            
            statement = self.case(
                cases=[
                    # for all users are in allowed privates, return true
                    (f"{self.cast(val_name='user_id', casting_type='text')} in ({', '.join(s)})", 'true'),
                ],
                # default is true only if private is not true (means: it is public)
                default=f"{self.cast(val_name='is_private is not true', casting_type='bool')}"
            )

            conditions.append(statement)

        return conditions, params


    async def search(self) -> List[Video]:
        conditions, params = self.build_query_conditions_params()

        # keep limit as the last param, and use it only on select statement
        # it is the last sql expression and it is also a condition by itself
        params.append(self.requested_limit)

        # default to true to prevent query crash for invalid WHERE syntax where conditions are empty
        where_condition = 'true'
        if 0 < len(conditions):
            where_condition = f'{nl()}AND '.join(conditions)
        
        videos = await self.get_connection_fn().query([
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
                WHERE {where_condition}
                ORDER BY pagination_index DESC
                LIMIT %s""",
                tuple(params)
            )
        ])

        return list(map(self.__prase_db_records_into_classes, videos))
    

    async def delete(self) -> None:
        await super().delete(stage=VideoStages.READY.value)
    

    async def update(self, new_desired_state: Dict) -> None:
        await super().update(new_desired_state=new_desired_state, stage=VideoStages.READY.value)


    def with_hash(self, id: UUID) -> VideosDescriberPG:
        return super().with_hash(id=id)


    def owned_by(self, user_id: UUID) -> VideosDescriberPG:
        return super().with_hash(user_id=user_id)


    def not_owned_by(self, user_id: UUID) -> VideosDescriberPG:
        if user_id is not None:
            self.excluded_user_ids.append(user_id)
        return self


    def include_privates_of(self, user_id: UUID) -> VideosDescriberPG:
        if user_id is not None:
            self.allowed_privates_of_user_ids.append(user_id)
        return self


    def filter_unlisted(self, flag: bool = True) -> VideosDescriberPG:
        self.unlisted_should_be_hidden = flag
        return self


    def unfilter_privates(self, flag: bool = True) -> VideosDescriberPG:
        self.allow_privates_globally = flag
        return self

    
    def paginate(self, pagination_index_is_smaller_than: int) -> VideosDescriberPG:
        self.pagination_index_is_smaller_than = pagination_index_is_smaller_than
        return self
    

    def limit(self, limit: int) -> VideosDescriberPG:
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
            storage_object_key=video[8],
            storage_thumbnail_key=video[9],
            upload_time=video[10],
            is_private=video[11],
            listing_time=video[12],
            pagination_index=video[13]
        )
