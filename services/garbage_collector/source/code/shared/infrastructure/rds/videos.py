from shared.infrastructure.rds.database import Database
from shared.models.garbage.enums import GarbageTypes
from shared.infrastructure.rds import tables
import aiopg
from functools import partial
from typing import List, Optional
from shared.models.garbage.video import Video


class VideosDatabase(Database):
   
    async def get_marked_for_delete(self, limit: int = 100, connection: Optional[aiopg.Connection] = None) -> List[Video]:
        """Gets videos which are marked as deleted."""

        if limit <= 0:
            raise ValueError('Limit must be greater than 0')
        
        return await self.dml(
            connection=connection,
            action=partial(self._get_marked_for_delete, limit=limit)
        )


    async def _get_marked_for_delete(self, limit: int, cursor: aiopg.Cursor) -> List[Video]:
        await cursor.execute(
            '\n'.join([
                'SELECT',
                'user_id,',
                'hash_id,',
                'thumbnail_url,',
                'storage_object_key,',
                'storage_thumbnail_key',
                f'FROM {tables.VIDEOS_TABLE}',
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
                    type=GarbageTypes.VIDEO_DELETE,
                    row=row
                ),
                await cursor.fetchall()
            )
        )


    async def delete(self, video: Video, connection: Optional[aiopg.Connection] = None) -> None:
        """Deletes videos which are marked as deleted."""

        await self.dml(
            connection=connection,
            action=partial(self._delete, video=video)
        )


    async def _delete(self, video: Video, cursor: aiopg.Cursor) -> None:
        await cursor.execute(
            '\n'.join([
                'DELETE FROM',
                f'{tables.VIDEOS_TABLE}',
                'WHERE user_id = %s AND hash_id = %s'
            ]),
            (video.user_id, video.hash_id)
        )


    def parse_row(self, type: GarbageTypes, row: tuple) -> Video:
        return Video(
            type=type,
            user_id=row[0],
            hash_id=row[1],
            thumbnail_url=row[2],
            storage_object_key=row[3],
            storage_thumbnail_key=row[4],
        )
