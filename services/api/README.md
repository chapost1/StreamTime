# API Web Server Service

#### Table of Contents
- [Service Diagram](#diagram)
- [Layers Key Points](#layers_key_points)

## Service Diagram <a name="diagram"></a>
<hr>

#### Heavily influenced by Robert C. Martin (Uncle Bob), <a href="https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html">The Clean Architecture</a>

This Diagram should explain the relation between the app layers.

![Api Web Server Service Diagram](./abstract_web_api_architecture_diagram.jpg)

## Layers <a name="layers_key_points"></a>
<hr>

#### Layers Table of Contents
- [External Systems](#external_systems)
- [Use Cases](#use_cases)
- [Entities](#entities)


## External Systems  <a name="external_systems"></a>

    This layer is for egress/ingress usages and is the outer-most layer, which is most prone to change.
    It includes sub-layers such as:
        - http_network_interface
        - data_access
        - integrations with 3-parties

### Sub Layers Table of Contents
- [Routers](#routers)
- [Data Access](#data_access)



### Routers  <a name="routers"></a>

    The Routers are basically a layer inside of the External Systems layer.

    It can be found under the sub-layer http_network_interface.

Key notes:

:old_key: The routers are the entrypoint for the HTTP interface of the app.

:key: More technically, the routers are just a map between HTTP calls and use cases functions.

#### API HTTP Endpoints

    The best way to understand the API HTTP Endpoints is to spin up the service.
    Then, look at the Swagger page which can be found on the /docs endpoint

Alternatively, if you don't want to spin up the service, you can read about it <strong>[here](./openapi.md)</strong> using a simpler markdown version.

#### Where can I find the Routers in the source code?

A simplified version of the tree output beside to the entrypoint.py file:

```sh
|-- entrypoint.py
|-- external_systems
|   |-- http_network_interface
|       `-- routers # here
```


### Data Access <a name="data_access"></a>

    The Data Access is basically a layer (DAL) inside of the External Systems layer.

    This layer (Data Access) is responsible for the "low level" integration with databases & storages or similar.

#### Where can I find the DAL in the source code?

A simplified version of the tree output beside to the entrypoint.py file:

```sh
|-- entrypoint.py
|-- external_systems
|   `-- data_access # here
|   |   |-- rds
|   |   |-- storage
```

Currently the Concrete RDS implementation is Postgresql

It worth to mention, that its implementation uses a class which is called a "Describer"

It's code can be found under the pg directory of the RDS for any domain's entity.

It is in general sort of a builder pattern which is related to the specific app domain entity (i.e: videos) and its properties.

> Similar to ORM but more dedicated to the application domain and logic.

It lets the user (i.e: the get method of the videos database class) to build certain queries dynamically based on the arguments it pass to the describer, without the need to repeat writing similar logics for many use case's queries.

It's syntax may be similar to this:

```python
database.describe_videos()
.owned_by(user_id=user_id)
.filter_unlisted(flag=True)
.include_privates_of(user_id=authenticated_user_id)
.paginate(pagination_index_is_smaller_than=pagination_index_is_smaller_than)
.limit(limit=page_limit)
.search()
```

Notice that, as mentioned the syntax is related to the domain itself, it "describes" to the database how the records should look like.

Afterwards, it's possible to do some supported operations, such as Search, or Delete.

> Each domain entity has its own Describers (i.e: Videos)

The describers classes can be found here (relative to the DAL directroy):

```sh
|-- __init__.py
|-- rds
|   |-- pg
|   |   |-- __init__.py
|   |   |-- videos
|   |       |-- __init__.py
|   |       |-- database.py
|   |       `-- describers # here
|   |           |-- __init__.py
|   |           |-- test
|   |           |-- unprocessed_videos.py
|   |           |-- uploaded_videos.py
|   |           |-- videos.py
```



## Use Cases <a name="use_cases"></a>

    In general, this is the layer which is responsible to the business logic.

    It is dedicated to be domain driven.

    It means for example, if you look at the videos directories tree you can understand the use cases of the app.

### Where can I find the Use Cases in the source code?

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

Each Use case is a directory by itself and contains the followings:
- use_case.py: file which contains a use_case() funciton, which is the logic itself.
- test folder: unit tests for the specific use case.
- helpers (optional): helper functions which are needed to perform the use case
  these files are seperated for these purposes:
  - help maintain the use case simpler, so that it can use them as a black box.
  - be able to mock them and isolate the use case when testing it.
- __ init __ .py: is used to stitch the use case with its helpers before exporting it so any other layer can import it.


For example, the update_video use case directory in lower resolution:
 
```sh
|-- update_video
    |-- __init__.py
    |-- helpers
        |-- __init__.py
        |-- test
        |-- abstract.py
        |-- listed_videos_preparations.py
        |-- new_listing_preparations.py
        |-- parse_video_into_state_dict.py
    |-- test
    |-- use_case.py
```

## Entities <a name="entities"></a>

   The Entities layer contains the application/domain models for the service. The entities are a critical component of the service, as they define the core data and behavior of the service and provide the foundation for the other components to build upon.

> As This is the core of data of the service, it should change less frequently.

The Entities are typically defined using pydantic classes, to provide automatic type validations/basic functionality to each defined field.
This is the most 

The "entities" package is typically located within the service's source code tree, alongside the other components such as the routers and use cases. For example, the directory structure of the service may look something like this:

```sh
|-- entrypoint.py
|-- external_systems
|-- use_cases
`-- entities # here
|   |-- __init__.py
|   |-- videos.py
|   |-- storage.py
```

The "entities" package is typically imported and used by other components of the service, such as the use cases, to create and/or manipulate entity objects. For instance, a Video class can be created after searching the database, and reveal methods that can be used in the use cases layer.
Or for another example, the VideoPage class can calculate the next page based on the current videos that it compose.

Overall, the "entities" package is a key component of the service, as it defines the core data and behavior of the service and provides a consistent and standardized way to represent and manipulate the data within the service.
