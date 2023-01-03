from shared.rds.database import Database
from shared.models.garbage.enums import GarbageTypes
from shared.rds import tables
from typing import List
from shared.models.garbage.unprocessed_video import UnprocessedVideo
from common.environment import (
    MAX_VIDEO_PROCESSING_TIME_SECONDS,
    VIDEO_PROCESSING_INTERNAL_SERVER_ERROR_MESSAGE
)


class UnprocessedVideosDatabase(Database):
   
    def get_marked_for_delete(self, limit: int = 100) -> List[UnprocessedVideo]:
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

        return list(
            map(
                lambda row: self.parse_row(
                    type=GarbageTypes.UNPROCESSED_VIDEO_DELETE,
                    row=row
                ),
                videos
            )
        )


    def delete(self, video: UnprocessedVideo) -> None:
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
    

    def get_failed_to_process(self, limit: int = 100) -> List[UnprocessedVideo]:
        """Gets unprocessed videos which failed to process during max process time."""

        if limit <= 0:
            raise ValueError('Limit must be greater than 0')
        
        in_a_transaction = self.connection is not None

        if not in_a_transaction:
            self.begin()

        # add 10% to the max processing time to account for processing time
        safe_window_seconds = MAX_VIDEO_PROCESSING_TIME_SECONDS * 1.1

        self.execute(
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
        videos = self.fetchall()

        if not in_a_transaction:
            self.commit()

        return list(
            map(
                lambda row: self.parse_row(
                    type=GarbageTypes.UNPROCESSED_VIDEO_INTERNAL_SERVER_ERROR,
                    row=row
                ),
                videos
            )
        )


    def mark_as_internal_server_error(self, video: UnprocessedVideo) -> None:
        """Marks unprocessed videos as internal server error."""

        in_a_transaction = self.connection is not None

        if not in_a_transaction:
            self.begin()

        self.execute(
            '\n'.join([
                'UPDATE',
                f'{tables.UNPROCESSED_VIDEOS_TABLE}',
                'SET failure_reason = %s',
                'WHERE user_id = %s AND hash_id = %s'
            ]),
            (VIDEO_PROCESSING_INTERNAL_SERVER_ERROR_MESSAGE, video.user_id, video.hash_id)
        )

        if not in_a_transaction:
            self.commit()


    def parse_row(self, type: GarbageTypes, row: tuple) -> UnprocessedVideo:
        return UnprocessedVideo(
            type=type,
            user_id=row[0],
            hash_id=row[1],
        )
