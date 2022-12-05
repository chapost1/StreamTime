from uuid import UUID
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from external_systems.data_access.rds.abstract.videos import VideosDescriber


def describe(
    database: VideosDatabase,
    authenticated_user_id: UUID,
    user_id: UUID,
    pagination_index_is_smaller_than: int,
    page_limit: int
) -> VideosDescriber:
    return (
        database.describe_videos()
        .owned_by(user_id=user_id)
        .filter_unlisted(flag=True)
        .include_privates_of(user_id=authenticated_user_id)
        .paginate(pagination_index_is_smaller_than=pagination_index_is_smaller_than)
        .limit(limit=page_limit)
    )
