from shared.rds.database import Database
from shared.models.garbage.enums import GarbageTypes
from shared.rds import tables
import aiopg
from functools import partial
from typing import List, Optional
from shared.models.garbage.unprocessed_video import UnprocessedVideo
from common.environment import (
    MAX_VIDEO_PROCESSING_TIME_SECONDS,
    VIDEO_PROCESSING_INTERNAL_SERVER_ERROR_MESSAGE
)


class UnprocessedVideosDatabase(Database):
    """Unprocessed videos database."""
   
    async def get_marked_for_delete(self, limit: int = 100, connection: Optional[aiopg.Connection] = None) -> List[UnprocessedVideo]:
        """Gets unprocessed videos which are marked as deleted."""

        if limit <= 0:
            raise ValueError('Limit must be greater than 0')
        
        return await self.dml(
            connection=connection,
            action=partial(self._get_marked_for_delete, limit=limit)
        )

    
    async def _get_marked_for_delete(self, limit: int, cursor: aiopg.Cursor) -> List[UnprocessedVideo]:
        await cursor.execute(
            '\n'.join([
                'SELECT',
                'user_id,',
                'hash_id',
                f'FROM {tables.UNPROCESSED_VIDEOS_TABLE}',
                'WHERE deleted_at IS NOT null',
                'ORDER BY deleted_at ASC',
                'LIMIT %s',
                'FOR UPDATE'
            ]),
            (limit,)
        )

        return list(
            map(
                lambda row: self.parse_row(
                    type=GarbageTypes.UNPROCESSED_VIDEO_DELETE,
                    row=row
                ),
                await cursor.fetchall()
            )
        )


    async def delete(self, video: UnprocessedVideo, connection: Optional[aiopg.Connection] = None) -> None:
        """Deletes unprocessed videos which are marked as deleted."""

        await self.dml(
            connection=connection,
            action=partial(self._delete, video=video)
        )


    async def _delete(self, video: UnprocessedVideo, cursor: aiopg.Cursor) -> None:
        await cursor.execute(
            '\n'.join([
                'DELETE FROM',
                f'{tables.UNPROCESSED_VIDEOS_TABLE}',
                'WHERE user_id = %s AND hash_id = %s'
            ]),
            (video.user_id, video.hash_id)
        )


    async def get_failed_to_process(self, limit: int = 100, connection: Optional[aiopg.Connection] = None) -> List[UnprocessedVideo]:
        """Gets unprocessed videos which failed to process during max process time."""

        if limit <= 0:
            raise ValueError('Limit must be greater than 0')
        
        return await self.dml(
            connection=connection,
            action=partial(self._get_failed_to_process, limit=limit)
        )


    async def _get_failed_to_process(self, limit: int, cursor: aiopg.Cursor) -> List[UnprocessedVideo]:
        """Gets unprocessed videos which failed to process during max process time."""
        # add 10% to the max processing time to account for processing time
        safe_window_seconds = MAX_VIDEO_PROCESSING_TIME_SECONDS * 1.1

        await cursor.execute(
            '\n'.join([
                'SELECT',
                'user_id,',
                'hash_id',
                f'FROM {tables.UNPROCESSED_VIDEOS_TABLE}',
                'WHERE failure_reason IS null',
                # videos which have been processing for more than x seconds
                'AND (extract(epoch from now())::int - extract(epoch from upload_time)::int) > %s'
                'ORDER BY upload_time ASC',
                'LIMIT %s',
                'FOR UPDATE'
            ]),
            (safe_window_seconds, limit,)
        )

        return list(
            map(
                lambda row: self.parse_row(
                    type=GarbageTypes.UNPROCESSED_VIDEO_INTERNAL_SERVER_ERROR,
                    row=row
                ),
                await cursor.fetchall()
            )
        )

    async def mark_as_internal_server_error(self, video: UnprocessedVideo, connection: Optional[aiopg.Connection] = None) -> None:
        """Marks unprocessed videos as internal server error."""

        await self.dml(
            connection=connection,
            action=partial(self._mark_as_internal_server_error, video=video)
        )

    
    async def _mark_as_internal_server_error(self, video: UnprocessedVideo, cursor: aiopg.Cursor) -> None:
        """Marks unprocessed videos as internal server error."""

        await cursor.execute(
            '\n'.join([
                'UPDATE',
                f'{tables.UNPROCESSED_VIDEOS_TABLE}',
                'SET failure_reason = %s',
                'WHERE user_id = %s AND hash_id = %s'
            ]),
            (VIDEO_PROCESSING_INTERNAL_SERVER_ERROR_MESSAGE, video.user_id, video.hash_id)
        )


    def parse_row(self, type: GarbageTypes, row: tuple) -> UnprocessedVideo:
        return UnprocessedVideo(
            type=type,
            user_id=row[0],
            hash_id=row[1],
        )
