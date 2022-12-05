from uuid import UUID
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from external_systems.data_access.rds.abstract.videos import VideosDescriber


def describe_unprocessed_videos(
    database: VideosDatabase,
    authenticated_user_id: UUID
) -> VideosDescriber:
    return (
        database.describe_unprocessd_videos()
        .owned_by(user_id=authenticated_user_id)
    )


def describe_videos(
    database: VideosDatabase,
    authenticated_user_id: UUID
):
    return (
        database.describe_videos()
        .owned_by(user_id=authenticated_user_id)
        .include_privates_of(user_id=authenticated_user_id)
    )
