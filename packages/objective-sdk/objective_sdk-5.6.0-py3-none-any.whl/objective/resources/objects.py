# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ..types import object_list_params, object_batch_params, object_create_params, object_update_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.object_get_response import ObjectGetResponse
from ..types.object_list_response import ObjectListResponse
from ..types.object_batch_response import ObjectBatchResponse
from ..types.object_create_response import ObjectCreateResponse
from ..types.object_delete_response import ObjectDeleteResponse
from ..types.object_status_response import ObjectStatusResponse
from ..types.object_update_response import ObjectUpdateResponse
from ..types.object_delete_all_response import ObjectDeleteAllResponse

__all__ = ["ObjectsResource", "AsyncObjectsResource"]


class ObjectsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ObjectsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/objective-inc/objective-python#accessing-raw-response-data-eg-headers
        """
        return ObjectsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ObjectsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/objective-inc/objective-python#with_streaming_response
        """
        return ObjectsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectCreateResponse:
        """Creates an Object.

        The request body is any JSON object.

        This is schemaless.

        Returns a JSON object with an 'id' set to the newly created ID. The 'Location'
        HTTP response header is set to the URL of the new Object, which contains the
        same ID.

        This is an asynchronous operation. If the Object already exists, a duplicate
        will be created with a new ID.

        ## Using your own IDs

        This operation adds the object to the catalog and creates a unique ID for the
        object. You must store this ID in order to refer to the object in future
        operations (e.g. DELETE / PATCH). If you wish to create an Object with an ID of
        your choice, you must
        [use a PUT instead](/apis/ingestion/partially-update-object-in-the-object-store)
        -- this creates an ID and returns it to you.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/objects",
            body=maybe_transform(body, object_create_params.ObjectCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectCreateResponse,
        )

    def update(
        self,
        object_id: str,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectUpdateResponse:
        """
        Upserts the Object to the Object Store.

        This creates the Object if it does not exist, or replaces its contents entirely
        if it does exist. This is schemaless. If you want to specify the ID at creation
        time, you must use this PUT instead of the POST, because the POST endpoint
        creates an ID.

        Returns an empty JSON object (`{}`). Sets the 'Location' HTTP response header to
        the URL of the upserted Object.

        This is an asynchronous operation.

        ## Examples

        When upserting objects, it is important to explicitly set the `id` field in your
        request. If no `id` is set the upsert endpoint will also generate a unique ID
        for the Object. The `id` field is used to match the Object to the existing
        Object in the Object Store.

        In these examples, we'll be using `bash` commands. But they should be adaptable
        to any programming language.

        ### Upserting a single Object

        ```bash
        #!/bin/bash
        API_KEY='YOUR_API_KEY'
        OBJECT_ID='sku_123456'
        OBJECT='{"name": "White T-Shirt", "color": "white", "size": "medium", "price": 10.99}'

        curl -X PUT   "https://api.objective.inc/v1/objects/$OBJECT_ID"   -H "Authorization: Bearer $API_KEY"   -H "Content-Type: application/json"   -d "$OBJECT"
        ```

        ### Upserting multiple Objects from JSON data with existing IDs

        Often times your data will already have an ID field. In this case, you can use
        your existing ID field to upsert the Object to the Object Store. In this
        example, we will use the `product_id` field as the `id` for upserting the
        Objects. For this to work, you'll want to make sure your system has
        [jq](https://jqlang.github.io/jq/) installed.

        ```bash
        API_KEY="YOUR_API_KEY"
        # JSON data containing multiple objects
        JSON_DATA='[
            {"product_id": "sku_123456", "name": "White T-Shirt", "color": "white", "size": "medium", "price": 10.99},
            {"product_id": "sku_123457", "name": "Black T-Shirt", "color": "black", "size": "large", "price": 11.99}
        ]'

        # Loop through each object in the JSON array
        echo "$JSON_DATA" | jq -c '.[]' | while read -r object; do
            # Extract the id from the object
            id=$(echo "$object" | jq -r '.product_id')

            # Make the curl request
            response=$(curl -s -o /dev/null -w "%{http_code}" -X PUT         "https://api.objective.inc/v1/objects/$id"         -H "Authorization: Bearer $API_KEY"         -H "Content-Type: application/json"         -d "$object")
        done
        ```

        ### Batch Upserting Objects from JSON data

        Building on the previous example, this one downloads a JSON file with 10,000
        objects and upserts them to the Object Store in parallel.

        ```bash
        #!/bin/bash
        API_KEY='YOUR_API_KEY'
        # Download JSON data from the provided URL
        JSON_DATA=$(curl -s https://d11p8vtjlacpl4.cloudfront.net/demos/ecommerce/hm-10k.json)

        # Check if the download was successful
        if [ $? -ne 0 ]; then
            exit 1
        fi

        process_object() {
            local object="$1"
            id=$(echo "$object" | jq -r '.article_id')
            status_code=$(curl -s -o /dev/null -w "%{http_code}" -X PUT         "https://api.objective.inc/v1/objects/$id"         -H "Authorization: Bearer $API_KEY"         -H "Content-Type: application/json"         -d "$object")
            if [ "$status_code" != "202" ]; then
                echo "Error processing object $id: Status code $status_code"
            fi
        }

        export -f process_object
        export API_KEY

        # Process objects in parallel, 100 at a time
        echo "$JSON_DATA" | jq -c '.[]' | xargs -P 100 -I -J{} bash -c 'process_object "{}"'
        ```

        Args:
          object_id: Object ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not object_id:
            raise ValueError(f"Expected a non-empty value for `object_id` but received {object_id!r}")
        return self._put(
            f"/objects/{object_id}",
            body=maybe_transform(body, object_update_params.ObjectUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectUpdateResponse,
        )

    def list(
        self,
        *,
        cursor: str | NotGiven = NOT_GIVEN,
        include_metadata: bool | NotGiven = NOT_GIVEN,
        include_object: bool | NotGiven = NOT_GIVEN,
        limit: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectListResponse:
        """
        List all objects in the object store.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/objects",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "include_metadata": include_metadata,
                        "include_object": include_object,
                        "limit": limit,
                    },
                    object_list_params.ObjectListParams,
                ),
            ),
            cast_to=ObjectListResponse,
        )

    def delete(
        self,
        object_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectDeleteResponse:
        """
        Schedules an Object in the Object Store for deletion.

        This is an asynchronous operation. If no such Object exists, this does nothing.

        Search results and other APIs are cached for several minutes not just by this
        API but possibly by third- party servers out of our control. See
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
        regarding the standard HTTP caching mechanism that we use to improve
        performance.

        The same ID may be used later to create a new Object, the same or different.

        Returns an empty JSON object (`{}`).

        Args:
          object_id: Object ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not object_id:
            raise ValueError(f"Expected a non-empty value for `object_id` but received {object_id!r}")
        return self._delete(
            f"/objects/{object_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectDeleteResponse,
        )

    def batch(
        self,
        *,
        operations: Iterable[object_batch_params.Operation],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectBatchResponse:
        """
        Batch operations on objects.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/objects:batch",
            body=maybe_transform({"operations": operations}, object_batch_params.ObjectBatchParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectBatchResponse,
        )

    def delete_all(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectDeleteAllResponse:
        """
        Schedules all Objects in the Object Store for deletion.

        This is an asynchronous operation. If no Objects exist, this does nothing.

        Returns a `request-id` JSON object (`{"request-id": "..."}`).

        ## Example

        > This command will delete all Objects from your Object Store. This operation is
        > not reversable.

        ```bash
        curl -X POST -H "Authorization: Bearer YOUR_API_KEY" https://api.objective.inc/v1/objects:deleteAll
        ```
        """
        return self._post(
            "/objects:deleteAll",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectDeleteAllResponse,
        )

    def get(
        self,
        object_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectGetResponse:
        """
        Get an Object by ID.

        ## Status

        Objects within an index can have 4 different status types.

        1. `UPLOADED` - The state of an object that is in the object store but is
           pending processing.
        2. `PROCESSING` - The state of an object that is currently being indexed.
        3. `READY` - The state of an object that is live and searchable.
        4. `ERROR` - The state of an object that has encountered errors during
           processing; you can find out more information about the error by using the
           object status API.

        Args:
          object_id: Object ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not object_id:
            raise ValueError(f"Expected a non-empty value for `object_id` but received {object_id!r}")
        return self._get(
            f"/objects/{object_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectGetResponse,
        )

    def status(
        self,
        object_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectStatusResponse:
        """Get an Object's indexing status by ID.

        Used to view the indexing status of an
        individual Object across all Indexes that are marked to index the object.

        ## Status

        Objects within an index can have 4 different status types.

        1. `UPLOADED` - The state of an object that is in the object store but is
           pending processing.
        2. `PROCESSING` - The state of an object that is currently being indexed.
        3. `READY` - The state of an object that is live and searchable.
        4. `ERROR` - The state of an object that has encountered errors during
           processing; you can find out more information about the error by using the
           object status API.

        Args:
          object_id: Object ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not object_id:
            raise ValueError(f"Expected a non-empty value for `object_id` but received {object_id!r}")
        return self._get(
            f"/objects/{object_id}/status",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectStatusResponse,
        )


class AsyncObjectsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncObjectsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/objective-inc/objective-python#accessing-raw-response-data-eg-headers
        """
        return AsyncObjectsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncObjectsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/objective-inc/objective-python#with_streaming_response
        """
        return AsyncObjectsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectCreateResponse:
        """Creates an Object.

        The request body is any JSON object.

        This is schemaless.

        Returns a JSON object with an 'id' set to the newly created ID. The 'Location'
        HTTP response header is set to the URL of the new Object, which contains the
        same ID.

        This is an asynchronous operation. If the Object already exists, a duplicate
        will be created with a new ID.

        ## Using your own IDs

        This operation adds the object to the catalog and creates a unique ID for the
        object. You must store this ID in order to refer to the object in future
        operations (e.g. DELETE / PATCH). If you wish to create an Object with an ID of
        your choice, you must
        [use a PUT instead](/apis/ingestion/partially-update-object-in-the-object-store)
        -- this creates an ID and returns it to you.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/objects",
            body=await async_maybe_transform(body, object_create_params.ObjectCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectCreateResponse,
        )

    async def update(
        self,
        object_id: str,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectUpdateResponse:
        """
        Upserts the Object to the Object Store.

        This creates the Object if it does not exist, or replaces its contents entirely
        if it does exist. This is schemaless. If you want to specify the ID at creation
        time, you must use this PUT instead of the POST, because the POST endpoint
        creates an ID.

        Returns an empty JSON object (`{}`). Sets the 'Location' HTTP response header to
        the URL of the upserted Object.

        This is an asynchronous operation.

        ## Examples

        When upserting objects, it is important to explicitly set the `id` field in your
        request. If no `id` is set the upsert endpoint will also generate a unique ID
        for the Object. The `id` field is used to match the Object to the existing
        Object in the Object Store.

        In these examples, we'll be using `bash` commands. But they should be adaptable
        to any programming language.

        ### Upserting a single Object

        ```bash
        #!/bin/bash
        API_KEY='YOUR_API_KEY'
        OBJECT_ID='sku_123456'
        OBJECT='{"name": "White T-Shirt", "color": "white", "size": "medium", "price": 10.99}'

        curl -X PUT   "https://api.objective.inc/v1/objects/$OBJECT_ID"   -H "Authorization: Bearer $API_KEY"   -H "Content-Type: application/json"   -d "$OBJECT"
        ```

        ### Upserting multiple Objects from JSON data with existing IDs

        Often times your data will already have an ID field. In this case, you can use
        your existing ID field to upsert the Object to the Object Store. In this
        example, we will use the `product_id` field as the `id` for upserting the
        Objects. For this to work, you'll want to make sure your system has
        [jq](https://jqlang.github.io/jq/) installed.

        ```bash
        API_KEY="YOUR_API_KEY"
        # JSON data containing multiple objects
        JSON_DATA='[
            {"product_id": "sku_123456", "name": "White T-Shirt", "color": "white", "size": "medium", "price": 10.99},
            {"product_id": "sku_123457", "name": "Black T-Shirt", "color": "black", "size": "large", "price": 11.99}
        ]'

        # Loop through each object in the JSON array
        echo "$JSON_DATA" | jq -c '.[]' | while read -r object; do
            # Extract the id from the object
            id=$(echo "$object" | jq -r '.product_id')

            # Make the curl request
            response=$(curl -s -o /dev/null -w "%{http_code}" -X PUT         "https://api.objective.inc/v1/objects/$id"         -H "Authorization: Bearer $API_KEY"         -H "Content-Type: application/json"         -d "$object")
        done
        ```

        ### Batch Upserting Objects from JSON data

        Building on the previous example, this one downloads a JSON file with 10,000
        objects and upserts them to the Object Store in parallel.

        ```bash
        #!/bin/bash
        API_KEY='YOUR_API_KEY'
        # Download JSON data from the provided URL
        JSON_DATA=$(curl -s https://d11p8vtjlacpl4.cloudfront.net/demos/ecommerce/hm-10k.json)

        # Check if the download was successful
        if [ $? -ne 0 ]; then
            exit 1
        fi

        process_object() {
            local object="$1"
            id=$(echo "$object" | jq -r '.article_id')
            status_code=$(curl -s -o /dev/null -w "%{http_code}" -X PUT         "https://api.objective.inc/v1/objects/$id"         -H "Authorization: Bearer $API_KEY"         -H "Content-Type: application/json"         -d "$object")
            if [ "$status_code" != "202" ]; then
                echo "Error processing object $id: Status code $status_code"
            fi
        }

        export -f process_object
        export API_KEY

        # Process objects in parallel, 100 at a time
        echo "$JSON_DATA" | jq -c '.[]' | xargs -P 100 -I -J{} bash -c 'process_object "{}"'
        ```

        Args:
          object_id: Object ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not object_id:
            raise ValueError(f"Expected a non-empty value for `object_id` but received {object_id!r}")
        return await self._put(
            f"/objects/{object_id}",
            body=await async_maybe_transform(body, object_update_params.ObjectUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectUpdateResponse,
        )

    async def list(
        self,
        *,
        cursor: str | NotGiven = NOT_GIVEN,
        include_metadata: bool | NotGiven = NOT_GIVEN,
        include_object: bool | NotGiven = NOT_GIVEN,
        limit: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectListResponse:
        """
        List all objects in the object store.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/objects",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "cursor": cursor,
                        "include_metadata": include_metadata,
                        "include_object": include_object,
                        "limit": limit,
                    },
                    object_list_params.ObjectListParams,
                ),
            ),
            cast_to=ObjectListResponse,
        )

    async def delete(
        self,
        object_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectDeleteResponse:
        """
        Schedules an Object in the Object Store for deletion.

        This is an asynchronous operation. If no such Object exists, this does nothing.

        Search results and other APIs are cached for several minutes not just by this
        API but possibly by third- party servers out of our control. See
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
        regarding the standard HTTP caching mechanism that we use to improve
        performance.

        The same ID may be used later to create a new Object, the same or different.

        Returns an empty JSON object (`{}`).

        Args:
          object_id: Object ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not object_id:
            raise ValueError(f"Expected a non-empty value for `object_id` but received {object_id!r}")
        return await self._delete(
            f"/objects/{object_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectDeleteResponse,
        )

    async def batch(
        self,
        *,
        operations: Iterable[object_batch_params.Operation],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectBatchResponse:
        """
        Batch operations on objects.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/objects:batch",
            body=await async_maybe_transform({"operations": operations}, object_batch_params.ObjectBatchParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectBatchResponse,
        )

    async def delete_all(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectDeleteAllResponse:
        """
        Schedules all Objects in the Object Store for deletion.

        This is an asynchronous operation. If no Objects exist, this does nothing.

        Returns a `request-id` JSON object (`{"request-id": "..."}`).

        ## Example

        > This command will delete all Objects from your Object Store. This operation is
        > not reversable.

        ```bash
        curl -X POST -H "Authorization: Bearer YOUR_API_KEY" https://api.objective.inc/v1/objects:deleteAll
        ```
        """
        return await self._post(
            "/objects:deleteAll",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectDeleteAllResponse,
        )

    async def get(
        self,
        object_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectGetResponse:
        """
        Get an Object by ID.

        ## Status

        Objects within an index can have 4 different status types.

        1. `UPLOADED` - The state of an object that is in the object store but is
           pending processing.
        2. `PROCESSING` - The state of an object that is currently being indexed.
        3. `READY` - The state of an object that is live and searchable.
        4. `ERROR` - The state of an object that has encountered errors during
           processing; you can find out more information about the error by using the
           object status API.

        Args:
          object_id: Object ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not object_id:
            raise ValueError(f"Expected a non-empty value for `object_id` but received {object_id!r}")
        return await self._get(
            f"/objects/{object_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectGetResponse,
        )

    async def status(
        self,
        object_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectStatusResponse:
        """Get an Object's indexing status by ID.

        Used to view the indexing status of an
        individual Object across all Indexes that are marked to index the object.

        ## Status

        Objects within an index can have 4 different status types.

        1. `UPLOADED` - The state of an object that is in the object store but is
           pending processing.
        2. `PROCESSING` - The state of an object that is currently being indexed.
        3. `READY` - The state of an object that is live and searchable.
        4. `ERROR` - The state of an object that has encountered errors during
           processing; you can find out more information about the error by using the
           object status API.

        Args:
          object_id: Object ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not object_id:
            raise ValueError(f"Expected a non-empty value for `object_id` but received {object_id!r}")
        return await self._get(
            f"/objects/{object_id}/status",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectStatusResponse,
        )


class ObjectsResourceWithRawResponse:
    def __init__(self, objects: ObjectsResource) -> None:
        self._objects = objects

        self.create = to_raw_response_wrapper(
            objects.create,
        )
        self.update = to_raw_response_wrapper(
            objects.update,
        )
        self.list = to_raw_response_wrapper(
            objects.list,
        )
        self.delete = to_raw_response_wrapper(
            objects.delete,
        )
        self.batch = to_raw_response_wrapper(
            objects.batch,
        )
        self.delete_all = to_raw_response_wrapper(
            objects.delete_all,
        )
        self.get = to_raw_response_wrapper(
            objects.get,
        )
        self.status = to_raw_response_wrapper(
            objects.status,
        )


class AsyncObjectsResourceWithRawResponse:
    def __init__(self, objects: AsyncObjectsResource) -> None:
        self._objects = objects

        self.create = async_to_raw_response_wrapper(
            objects.create,
        )
        self.update = async_to_raw_response_wrapper(
            objects.update,
        )
        self.list = async_to_raw_response_wrapper(
            objects.list,
        )
        self.delete = async_to_raw_response_wrapper(
            objects.delete,
        )
        self.batch = async_to_raw_response_wrapper(
            objects.batch,
        )
        self.delete_all = async_to_raw_response_wrapper(
            objects.delete_all,
        )
        self.get = async_to_raw_response_wrapper(
            objects.get,
        )
        self.status = async_to_raw_response_wrapper(
            objects.status,
        )


class ObjectsResourceWithStreamingResponse:
    def __init__(self, objects: ObjectsResource) -> None:
        self._objects = objects

        self.create = to_streamed_response_wrapper(
            objects.create,
        )
        self.update = to_streamed_response_wrapper(
            objects.update,
        )
        self.list = to_streamed_response_wrapper(
            objects.list,
        )
        self.delete = to_streamed_response_wrapper(
            objects.delete,
        )
        self.batch = to_streamed_response_wrapper(
            objects.batch,
        )
        self.delete_all = to_streamed_response_wrapper(
            objects.delete_all,
        )
        self.get = to_streamed_response_wrapper(
            objects.get,
        )
        self.status = to_streamed_response_wrapper(
            objects.status,
        )


class AsyncObjectsResourceWithStreamingResponse:
    def __init__(self, objects: AsyncObjectsResource) -> None:
        self._objects = objects

        self.create = async_to_streamed_response_wrapper(
            objects.create,
        )
        self.update = async_to_streamed_response_wrapper(
            objects.update,
        )
        self.list = async_to_streamed_response_wrapper(
            objects.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            objects.delete,
        )
        self.batch = async_to_streamed_response_wrapper(
            objects.batch,
        )
        self.delete_all = async_to_streamed_response_wrapper(
            objects.delete_all,
        )
        self.get = async_to_streamed_response_wrapper(
            objects.get,
        )
        self.status = async_to_streamed_response_wrapper(
            objects.status,
        )
