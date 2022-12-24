# FastAPI

> Version 0.1.0

## Path Table

| Method | Path | Description |
| --- | --- | --- |
| GET | [/health_check](#gethealth_check) | Health Check |
| GET | [/](#get) | Redirect To Health Check |
| GET | [/video/explore/](#getvideoexplore) | Explore Listed Videos |
| GET | [/video/upload/](#getvideoupload) | Get Upload Video Signed Instructions |
| GET | [/video/upload/config](#getvideouploadconfig) | Get Video Upload Config |
| GET | [/video/my/](#getvideomy) | Get Authenticated User Videos |
| PUT | [/video/my/{hash_id}](#putvideomyhash_id) | Update Video |
| DELETE | [/video/my/{hash_id}](#deletevideomyhash_id) | Delete Video |
| GET | [/video/user/{user_id}](#getvideouseruser_id) | Get Specific User Videos |
| GET | [/video/watch/](#getvideowatch) | Get Watch Video Record |

## Reference Table

| Name | Path | Description |
| --- | --- | --- |
| FileUploadSignedInstructions | [#/components/schemas/FileUploadSignedInstructions](#componentsschemasfileuploadsignedinstructions) |  |
| HTTPValidationError | [#/components/schemas/HTTPValidationError](#componentsschemashttpvalidationerror) |  |
| UnprocessedVideo | [#/components/schemas/UnprocessedVideo](#componentsschemasunprocessedvideo) |  |
| UserVideosList | [#/components/schemas/UserVideosList](#componentsschemasuservideoslist) |  |
| ValidationError | [#/components/schemas/ValidationError](#componentsschemasvalidationerror) |  |
| Video | [#/components/schemas/Video](#componentsschemasvideo) |  |
| VideoUploadConfigRecord | [#/components/schemas/VideoUploadConfigRecord](#componentsschemasvideouploadconfigrecord) |  |
| VideosPage | [#/components/schemas/VideosPage](#componentsschemasvideospage) |  |
| WatchVideoRecord | [#/components/schemas/WatchVideoRecord](#componentsschemaswatchvideorecord) |  |

## Path Details

***

### [GET]/health_check

- Summary  
Health Check

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

***

### [GET]/

- Summary  
Redirect To Health Check

#### Responses

- 200 Successful Response

`application/json`

```ts
{}
```

***

### [GET]/video/explore/

- Summary  
Explore Listed Videos

#### Parameters(Query)

```ts
next?: string
```

```ts
include_my?: boolean
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  videos: {
    hash_id?: string
    user_id?: string
    file_name?: string
    upload_time?: string
    title?: string
    description?: string
    size_in_bytes?: integer
    duration_seconds?: integer
    video_type?: string
    thumbnail_url?: string
    is_private?: boolean
    listing_time?: string
  }[]
  next?: string
}
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/video/upload/

- Summary  
Get Upload Video Signed Instructions

#### Parameters(Query)

```ts
file_content_type: string
```

```ts
file_name: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  url: string
  signatures: {
  }
}
```

- 400 Bad Request

- 401 Unauthorized

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/video/upload/config

- Summary  
Get Video Upload Config

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  max_size_in_bytes: integer
  valid_file_types?: string[]
}
```

- 401 Unauthorized

***

### [GET]/video/my/

- Summary  
Get Authenticated User Videos

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  unprocessed_videos: {
    hash_id?: string
    user_id?: string
    file_name?: string
    upload_time?: string
    failure_reason?: string
  }[]
  videos: {
    hash_id?: string
    user_id?: string
    file_name?: string
    upload_time?: string
    title?: string
    description?: string
    size_in_bytes?: integer
    duration_seconds?: integer
    video_type?: string
    thumbnail_url?: string
    is_private?: boolean
    listing_time?: string
  }[]
}
```

- 401 Unauthorized

***

### [PUT]/video/my/{hash_id}

- Summary  
Update Video

#### RequestBody

- application/json

```ts
{
  hash_id?: string
  user_id?: string
  file_name?: string
  upload_time?: string
  title?: string
  description?: string
  size_in_bytes?: integer
  duration_seconds?: integer
  video_type?: string
  thumbnail_url?: string
  is_private?: boolean
  listing_time?: string
}
```

#### Responses

- 204 Successful Response

- 400 Bad Request

- 401 Unauthorized

- 404 Not Found

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [DELETE]/video/my/{hash_id}

- Summary  
Delete Video

#### Responses

- 204 Successful Response

- 401 Unauthorized

- 404 Not Found

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

- 425 Too Early

***

### [GET]/video/user/{user_id}

- Summary  
Get Specific User Videos

#### Parameters(Query)

```ts
next?: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  videos: {
    hash_id?: string
    user_id?: string
    file_name?: string
    upload_time?: string
    title?: string
    description?: string
    size_in_bytes?: integer
    duration_seconds?: integer
    video_type?: string
    thumbnail_url?: string
    is_private?: boolean
    listing_time?: string
  }[]
  next?: string
}
```

- 404 Not Found

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [GET]/video/watch/

- Summary  
Get Watch Video Record

#### Parameters(Query)

```ts
user_id: string
```

```ts
hash_id: string
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  watchable_url: string
  video: {
    hash_id?: string
    user_id?: string
    file_name?: string
    upload_time?: string
    title?: string
    description?: string
    size_in_bytes?: integer
    duration_seconds?: integer
    video_type?: string
    thumbnail_url?: string
    is_private?: boolean
    listing_time?: string
  }
}
```

- 403 Forbidden

- 404 Not Found

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

## References

### #/components/schemas/FileUploadSignedInstructions

```ts
{
  url: string
  signatures: {
  }
}
```

### #/components/schemas/HTTPValidationError

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

### #/components/schemas/UnprocessedVideo

```ts
{
  hash_id?: string
  user_id?: string
  file_name?: string
  upload_time?: string
  failure_reason?: string
}
```

### #/components/schemas/UserVideosList

```ts
{
  unprocessed_videos: {
    hash_id?: string
    user_id?: string
    file_name?: string
    upload_time?: string
    failure_reason?: string
  }[]
  videos: {
    hash_id?: string
    user_id?: string
    file_name?: string
    upload_time?: string
    title?: string
    description?: string
    size_in_bytes?: integer
    duration_seconds?: integer
    video_type?: string
    thumbnail_url?: string
    is_private?: boolean
    listing_time?: string
  }[]
}
```

### #/components/schemas/ValidationError

```ts
{
  loc?: Partial(string) & Partial(integer)[]
  msg: string
  type: string
}
```

### #/components/schemas/Video

```ts
{
  hash_id?: string
  user_id?: string
  file_name?: string
  upload_time?: string
  title?: string
  description?: string
  size_in_bytes?: integer
  duration_seconds?: integer
  video_type?: string
  thumbnail_url?: string
  is_private?: boolean
  listing_time?: string
}
```

### #/components/schemas/VideoUploadConfigRecord

```ts
{
  max_size_in_bytes: integer
  valid_file_types?: string[]
}
```

### #/components/schemas/VideosPage

```ts
{
  videos: {
    hash_id?: string
    user_id?: string
    file_name?: string
    upload_time?: string
    title?: string
    description?: string
    size_in_bytes?: integer
    duration_seconds?: integer
    video_type?: string
    thumbnail_url?: string
    is_private?: boolean
    listing_time?: string
  }[]
  next?: string
}
```

### #/components/schemas/WatchVideoRecord

```ts
{
  watchable_url: string
  video: {
    hash_id?: string
    user_id?: string
    file_name?: string
    upload_time?: string
    title?: string
    description?: string
    size_in_bytes?: integer
    duration_seconds?: integer
    video_type?: string
    thumbnail_url?: string
    is_private?: boolean
    listing_time?: string
  }
}
```
