from external_systems.data_access.rds.pg.videos.database import VideosDatabasePG
from external_systems.data_access.rds.pg.connection.concrete import Connection
from external_systems.data_access.rds.pg.connection.abstract.conncetion import ConnectionProtocol
from entities.videos import (
    NextPage,
    VideosPage
)

def get_singleton_connection_instance() -> ConnectionProtocol:
    return Connection()

# exports an instance of Videos class
videos_db_client = VideosDatabasePG(
    get_connection_fn=get_singleton_connection_instance,
    next_page_text_decoder=NextPage,
    next_videos_page_calculator=VideosPage,
)
