from shared.rds.database import Database
from shared.models.garbage.enums import GarbageTypes
from shared.rds import tables
from typing import List
from shared.models.garbage.video import Video


class VideosDatabase(Database):
   
    def get_marked_for_delete(self, limit: int = 100) -> List[Video]:
        """Gets videos which are marked as deleted."""

        if limit <= 0:
            raise ValueError('Limit must be greater than 0')
        
        in_a_transaction = self.connection is not None

        if not in_a_transaction:
            self.begin()

        self.execute(
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
        videos = self.fetchall()

        if not in_a_transaction:
            self.commit()

        return list(
            map(
                lambda row: self.parse_row(
                    type=GarbageTypes.VIDEO_DELETE,
                    row=row
                ),
                videos
            )
        )


    def delete(self, video: Video) -> None:
        """Deletes videos which are marked as deleted."""

        in_a_transaction = self.connection is not None

        if not in_a_transaction:
            self.begin()

        self.execute(
            '\n'.join([
                'DELETE FROM',
                f'{tables.VIDEOS_TABLE}',
                'WHERE user_id = %s AND hash_id = %s'
            ]),
            (video.user_id, video.hash_id)
        )

        if not in_a_transaction:
            self.commit()
    

    def parse_row(self, type: GarbageTypes, row: tuple) -> Video:
        return Video(
            type=type,
            user_id=row[0],
            hash_id=row[1],
            thumbnail_url=row[2],
            storage_object_key=row[3],
            storage_thumbnail_key=row[4],
        )
