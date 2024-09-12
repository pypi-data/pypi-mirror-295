# Indexes

Types:

```python
from objective.types import (
    IndexCreateResponse,
    IndexListResponse,
    IndexDeleteResponse,
    IndexSearchResponse,
    IndexStatusResponse,
)
```

Methods:

- <code title="post /indexes">client.indexes.<a href="./src/objective/resources/indexes.py">create</a>(\*\*<a href="src/objective/types/index_create_params.py">params</a>) -> <a href="./src/objective/types/index_create_response.py">IndexCreateResponse</a></code>
- <code title="get /indexes">client.indexes.<a href="./src/objective/resources/indexes.py">list</a>() -> <a href="./src/objective/types/index_list_response.py">IndexListResponse</a></code>
- <code title="delete /indexes/{indexId}">client.indexes.<a href="./src/objective/resources/indexes.py">delete</a>(index_id) -> <a href="./src/objective/types/index_delete_response.py">IndexDeleteResponse</a></code>
- <code title="get /indexes/{indexId}/search">client.indexes.<a href="./src/objective/resources/indexes.py">search</a>(index_id, \*\*<a href="src/objective/types/index_search_params.py">params</a>) -> <a href="./src/objective/types/index_search_response.py">IndexSearchResponse</a></code>
- <code title="get /indexes/{indexId}/status">client.indexes.<a href="./src/objective/resources/indexes.py">status</a>(index_id) -> <a href="./src/objective/types/index_status_response.py">IndexStatusResponse</a></code>

# Objects

Types:

```python
from objective.types import (
    ObjectCreateResponse,
    ObjectUpdateResponse,
    ObjectListResponse,
    ObjectDeleteResponse,
    ObjectBatchResponse,
    ObjectDeleteAllResponse,
    ObjectGetResponse,
    ObjectStatusResponse,
)
```

Methods:

- <code title="post /objects">client.objects.<a href="./src/objective/resources/objects.py">create</a>(\*\*<a href="src/objective/types/object_create_params.py">params</a>) -> <a href="./src/objective/types/object_create_response.py">ObjectCreateResponse</a></code>
- <code title="put /objects/{objectId}">client.objects.<a href="./src/objective/resources/objects.py">update</a>(object_id, \*\*<a href="src/objective/types/object_update_params.py">params</a>) -> <a href="./src/objective/types/object_update_response.py">ObjectUpdateResponse</a></code>
- <code title="get /objects">client.objects.<a href="./src/objective/resources/objects.py">list</a>(\*\*<a href="src/objective/types/object_list_params.py">params</a>) -> <a href="./src/objective/types/object_list_response.py">ObjectListResponse</a></code>
- <code title="delete /objects/{objectId}">client.objects.<a href="./src/objective/resources/objects.py">delete</a>(object_id) -> <a href="./src/objective/types/object_delete_response.py">ObjectDeleteResponse</a></code>
- <code title="post /objects:batch">client.objects.<a href="./src/objective/resources/objects.py">batch</a>(\*\*<a href="src/objective/types/object_batch_params.py">params</a>) -> <a href="./src/objective/types/object_batch_response.py">ObjectBatchResponse</a></code>
- <code title="post /objects:deleteAll">client.objects.<a href="./src/objective/resources/objects.py">delete_all</a>() -> <a href="./src/objective/types/object_delete_all_response.py">ObjectDeleteAllResponse</a></code>
- <code title="get /objects/{objectId}">client.objects.<a href="./src/objective/resources/objects.py">get</a>(object_id) -> <a href="./src/objective/types/object_get_response.py">ObjectGetResponse</a></code>
- <code title="get /objects/{objectId}/status">client.objects.<a href="./src/objective/resources/objects.py">status</a>(object_id) -> <a href="./src/objective/types/object_status_response.py">ObjectStatusResponse</a></code>
