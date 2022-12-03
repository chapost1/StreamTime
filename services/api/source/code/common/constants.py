# Application mark for anonymous user
ANONYMOUS_USER = 'anonymous'

# presigned url maximum time to let user to perform upload action
# (to start it and then it is an atomic action)
MAXIMUM_SECONDS_TO_START_UPLOAD_A_FILE_USING_PRESIGNED_URL = 60 # ONE MINUTE

MAXIMUM_SECONDS_TILL_PRESIGNED_URL_EXPIRATION = 7 * 24 * 3600 # seven daya

# a numeric limit to select what is the limit of retrieving listed videos on one request
LISTED_VIDEOS_QUERY_PAGE_LIMIT = 15
