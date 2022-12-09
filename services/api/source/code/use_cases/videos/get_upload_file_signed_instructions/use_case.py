from uuid import UUID
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from external_systems.data_access.storage.abstract import Storage
from entities.storage import FileUploadSignedInstructions
from use_cases.videos.get_upload_file_signed_instructions.helpers.abstract import (
    AssertFileContentTypeFunction,
    GenerateNewVideoHashIdFunction
)


async def use_case(
    # creation scope
    database: VideosDatabase,
    storage: Storage,
    assert_file_content_type_fn: AssertFileContentTypeFunction,
    generate_new_video_hash_id_fn: GenerateNewVideoHashIdFunction,
    # usage scope
    authenticated_user_id: UUID,
    file_content_type: str
) -> FileUploadSignedInstructions:
    """
    Gets Signed Instructions to upload a Video

    A struct which holds a single use signed instructions to upload a Video
    It is needed to avoid free-access to the videos assets storage
    And yet to allow the users to upload a file using a single use signed instructions
    """

    assert_file_content_type_fn(file_content_type=file_content_type)

    hash_id = await generate_new_video_hash_id_fn(database=database, user_id=authenticated_user_id)

    object_key = f'{authenticated_user_id}/{hash_id}'

    return await storage.get_upload_file_signed_instructions(
        item_relative_path=object_key,
        file_content_type=file_content_type
    )
