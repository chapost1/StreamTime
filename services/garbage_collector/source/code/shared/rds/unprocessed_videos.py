from shared.rds.database import Database
from shared.garbage.enums import GarbageTypes
from shared.rds import tables
from typing import List
from shared.garbage.unprocessed_video import UnprocessedVideo


class UnprocessedVideosDatabase(Database):
   
    def get_garbage(self, limit: int = 100) -> List[UnprocessedVideo]:
        """Gets unprocessed videos which are marked as deleted."""

        if limit <= 0:
            raise ValueError('Limit must be greater than 0')
        
        in_a_transaction = self.connection is not None

        if not in_a_transaction:
            self.begin()

        self.execute(
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
        videos = self.fetchall()

        if not in_a_transaction:
            self.commit()

        return list(map(self.parse_row, videos))


    def delete_garbage(self, video: UnprocessedVideo) -> None:
        """Deletes unprocessed videos which are marked as deleted."""

        in_a_transaction = self.connection is not None

        if not in_a_transaction:
            self.begin()

        self.execute(
            '\n'.join([
                'DELETE FROM',
                f'{tables.UNPROCESSED_VIDEOS_TABLE}',
                'WHERE user_id = %s AND hash_id = %s'
            ]),
            (video.user_id, video.hash_id)
        )

        if not in_a_transaction:
            self.commit()
    

    def parse_row(self, row: tuple) -> UnprocessedVideo:
        return self.garbage_factory.create(
            type=GarbageTypes.UNPROCESSED_VIDEO.value,
            user_id=row[0],
            hash_id=row[1],
        )
