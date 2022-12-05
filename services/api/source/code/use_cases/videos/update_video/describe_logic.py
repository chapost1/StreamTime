from uuid import UUID
from external_systems.data_access.rds.abstract.videos import VideosDescriber
from external_systems.data_access.rds.abstract.videos import VideosDatabase


def describe(
    database: VideosDatabase,
    authenticated_user_id: UUID,
    hash_id: UUID
) -> VideosDescriber:
    return (
        database.describe_videos()
        .with_hash(id=hash_id)
        .owned_by(user_id=authenticated_user_id)
        .include_privates_of(user_id=authenticated_user_id)
    )
