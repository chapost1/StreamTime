## API Web Server

#### Heavily influenced by Robert C. Martin (Uncle Bob), <a href="https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html">The Clean Architecture</a>

### Service Diagram

This Diagram should explain the relation between the app layers.

![Web Api Service Diagram](./abstract_web_api_architecture_diagram.jpg)

### Table of Contents
- [Routers](#routers)
- [Use Cases](#use_cases)
- [Data Access](#data_access)


## Routers  <a name="routers"></a>

    The Routers are basically a layer inside of the External Systems layer.

    This layer (External Systems) is for egress/ingress usages and is the outer-most layer, which is most prone to change.

Key notes:

:old_key: The routers are the entrypoint for the HTTP interface of the app.

:key: More technically, the routers are just a map between HTTP calls and use cases functions.

    The best way to understand the API is to spin up the service.
    Then, look at the Swagger page which can be found on the /docs endpoint

Alternatively, if you don't want to spin up the service, you can read about it [here](./openapi.md) using a simpler markdown version.

### Where can I find the routers in the source code?

A simplified version of the tree output beside to the entrypoint.py file:

```sh
|-- entrypoint.py
|-- external_systems
|   |-- http_network_interface
|       `-- routers # here
```


## Use Cases <a name="use_cases"></a>

    In general, this is the layer which is responsible to the business logic.

    It is dedicated to be domain driven.

    It means for example, if you look at the videos directories tree you can understand the use cases of the app.

### Where can I find the routers in the source code?

A simplified version of the tree output beside to the entrypoint.py file:

> With dedication to the videos use cases as an example.

```sh
|-- entrypoint.py
`-- use_cases # here
    |-- __init__.py
    |-- videos
        |-- __init__.py
        |-- delete_video
        |-- explore_listed_videos
        |-- get_authenticated_user_videos
        |-- get_specific_user_listed_videos
        |-- get_upload_file_signed_instructions
        |-- get_video_upload_config
        |-- get_watch_video_record
        |-- update_video
```

Each Use case is built as another directory which has the followings:
- use_case.py: file which contains a use_case() funciton, which is the logic itself.
- test folder: unit tests for the specific use case and its helper functions.
- certain python files: basically helper functions which are needed to perform the use case
  these files are seperated for these purposes:
  - help maintain the use case simpler, so that it can use them as a black box.
  - be able to mock them and isolate the use case when testing it.
- db_describe_logic.py: not used in every use case. it's purposes is:
  - encapsulates the logic for calling the data access layer in the correct manner, it is seperated so it can be mocked easily.
  - it Creates a Database Describer object, which is discussed in the Data Access Layer section.
- __ init __ .py: is important because we can stitch the use case with its helpers before exporting it so any other layer can import it.


For example, the update_video use case directory in lower resolution:
 
```sh
|-- update_video
    |-- __init__.py
    |-- abstract_internals.py
    |-- db_describe_logic.py
    |-- listed_videos_preparations.py
    |-- new_listing_preparations.py
    |-- parse_video_into_state_dict.py
    |-- test
    |-- use_case.py
```

## Data Access <a name="data_access"></a>

    The Data Access is basically a layer inside of the External Systems layer.

    This layer (Data Access) is responsible for the "low level" integration with databases & storages or similar.

### Where can I find the routers in the source code?

A simplified version of the tree output beside to the entrypoint.py file:

```sh
|-- entrypoint.py
|-- external_systems
|   `-- data_access # here
|   |   |-- rds
|   |   |-- storage
```

It worth to mention, currently the Use Cases layer uses the RDS abstract protocol using something which is called a "Database Describer"

It's code can be found under the abstract directory of the RDS.

It is in general sort of a builder pattern which is related to the specific app domain (i.e: videos) and its properties.

> Similar to ORM but more dedicated to the application domain and logic.

It lets the user (i.e: Use Cases layer) to build certain queries dynamically without the need to create special function dedicated for this query in the Data Access layer, and yet to abstract the nitty-gritty parts from the DAL user.

It's syntax may be similar to this (usage example in the use case layer):

```python
database.describe_videos()
.owned_by(user_id=user_id)
.filter_unlisted(flag=True)
.include_privates_of(user_id=authenticated_user_id)
.paginate(pagination_index_is_smaller_than=pagination_index_is_smaller_than)
.limit(limit=page_limit)
```

Notice that, as mentioned the syntax is related to the domain itself, it "describes" to the database how the records should look like.

Afterwards, it's possible to do some supported operations, such as Search, or Delete.

> Each domain entity has its own Describers (i.e: Videos)

The abstract protocols can be found here (relative to the DAL directroy):

```sh
|-- __init__.py
|-- rds
|   |-- abstract
|   |   |-- __init__.py
|   |   |-- common_protocols.py
|   |   |-- videos
|   |       |-- __init__.py
|   |       |-- database.py
|   |       `-- describers # here
|   |           |-- __init__.py
|   |           |-- unprocessed_videos.py
|   |           |-- uploaded_videos.py
|   |           |-- videos.py
```

Notice that, the concrete implementations, i.e: of Postgres, can be found on the same files hierarchy under the pg directory.

it should be found on the path: (data_access/rds/pg)
