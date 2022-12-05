from uuid import UUID
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from external_systems.data_access.rds.abstract.videos import VideosDescriber


def describe(
    database: VideosDatabase,
    user_id_to_ignore: UUID,
    authenticated_user_to_allow_privates: UUID,
    pagination_index_is_smaller_than: int,
    page_limit: int
) -> VideosDescriber:
    return (
        database.describe_videos()
        .not_owned_by(user_id=user_id_to_ignore)
        .include_privates_of(user_id=authenticated_user_to_allow_privates)
        .filter_unlisted(flag=True)
        .paginate(pagination_index_is_smaller_than=pagination_index_is_smaller_than)
        .limit(limit=page_limit)
    )
