from external_systems.data_access.rds.abstract.videos import VideosDatabase
from external_systems.data_access.rds.pg.videos.describers import VideosDescriberPG
from external_systems.data_access.rds.pg.videos.describers import UnprocessedVideosDescriberPG
from external_systems.data_access.rds.pg.abstract_internals import GetConnectionFunction
from entities.videos.abstract_protocols import (
    NextPageTextDecoder,
    NextVideosPageCalculator
)
from entities.videos import VideoStages, Video, NextPage, UnprocessedVideo
from typing import List, Dict, Tuple, Optional
from external_systems.data_access.rds.pg.videos import tables
from uuid import UUID


class VideosDatabasePG:
    f"""
    VideosDatabase database class which implements the abstract protocol
    Uses postgres as a concrete implementation

    Abstract protocol docs:
    {VideosDatabase.__doc__}
    """

    get_connection_fn: GetConnectionFunction
    next_page_text_decoder: NextPageTextDecoder
    next_videos_page_calculator: NextVideosPageCalculator


    def __init__(
        self,
        get_connection_fn: GetConnectionFunction,
        next_page_text_decoder: NextPageTextDecoder,
        next_videos_page_calculator: NextVideosPageCalculator,
    ) -> None:
        self.get_connection_fn = get_connection_fn
        self.next_page_text_decoder = next_page_text_decoder
        self.next_videos_page_calculator = next_videos_page_calculator


    async def find_video_stage(self, user_id: UUID, hash_id: UUID) -> VideoStages:
        stages = await self.get_connection_fn().query([
            (
                f"""
                SELECT stage FROM (
                    SELECT '{VideoStages.UNPROCESSED.value}' as stage FROM {tables.UNPROCESSED_VIDEOS_TABLE}
                    WHERE user_id = %s
                    AND hash_id = %s
                ) as unprocessed
                UNION ALL
                SELECT stage FROM (
                    SELECT '{VideoStages.READY.value}' as stage FROM {tables.VIDEOS_TABLE}
                    WHERE user_id = %s
                    AND hash_id = %s
                ) as ready;
                """,
                tuple([user_id, hash_id, user_id, hash_id])
            )
        ])

        if len(stages) < 1:
            return None

        # each record first element is actually the stage key
        # maps records into this stage key element
        return list(map(lambda tup: tup[0], stages))


    async def get_videos(
        self,
        include_user_id: Optional[UUID] = None,
        include_hash_id: Optional[UUID] = None,
        ignore_user_id: Optional[UUID] = None,
        include_privates_of_user_id: Optional[UUID] = None,
        filter_unlisted: Optional[bool] = True,
        next: Optional[str] = None,
        page_limit: Optional[int] = None
    ) -> Tuple[List[Video], str]:

        curr_page: NextPage = self.next_page_text_decoder.decode(b64=next)

        videos: List[Video] = await (
            self._describe_videos()
            .owned_by(user_id=include_user_id)
            .not_owned_by(user_id=ignore_user_id)
            .with_hash(id=include_hash_id)
            .include_privates_of(user_id=include_privates_of_user_id)
            .filter_unlisted(flag=filter_unlisted)
            .paginate(pagination_index_is_smaller_than=curr_page.minimum_pagination_index)
            .limit(limit=page_limit)
            .search()
        )

        next_page: str = self.next_videos_page_calculator.calc_next_page(videos=videos)

        return videos, next_page


    async def update_video(
        self,
        user_id: UUID,
        hash_id: UUID,
        new_desired_state: Dict
    ) -> None:
        await (
            self._describe_videos()
            .with_hash(id=hash_id)
            .owned_by(user_id=user_id)
            .include_privates_of(user_id=user_id)
            .update(new_desired_state=new_desired_state)
        )


    async def delete_video(
        self,
        user_id: UUID,
        hash_id: UUID,
    ) -> None:
        await (
            self._describe_videos()
            .with_hash(id=hash_id)
            .owned_by(user_id=user_id)
            .include_privates_of(user_id=user_id)
            .delete()
        )


    async def get_unprocessed_videos(
        self,
        include_user_id: Optional[UUID] = None,
        include_hash_id: Optional[UUID] = None
    ) -> List[UnprocessedVideo]:
        return await (
            self._describe_unprocessd_videos()
            .owned_by(user_id=include_user_id)
            .with_hash(id=include_hash_id)
            .search()
        )


    async def delete_unprocessed_video(
        self,
        user_id: UUID,
        hash_id: UUID,
    ) -> None:
        await (
            self._describe_unprocessd_videos()
            .with_hash(id=hash_id)
            .owned_by(user_id=user_id)
            .delete()
        )


    def _describe_videos(self) -> VideosDescriberPG:
        return VideosDescriberPG(get_connection_fn=self.get_connection_fn)
    

    def _describe_unprocessd_videos(self) -> UnprocessedVideosDescriberPG:
        return UnprocessedVideosDescriberPG(get_connection_fn=self.get_connection_fn)
