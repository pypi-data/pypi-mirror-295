# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from objective import Objective, AsyncObjective
from tests.utils import assert_matches_type
from objective.types import (
    ObjectGetResponse,
    ObjectListResponse,
    ObjectBatchResponse,
    ObjectCreateResponse,
    ObjectDeleteResponse,
    ObjectStatusResponse,
    ObjectUpdateResponse,
    ObjectDeleteAllResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestObjects:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Objective) -> None:
        object_ = client.objects.create(
            body={},
        )
        assert_matches_type(ObjectCreateResponse, object_, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Objective) -> None:
        response = client.objects.with_raw_response.create(
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = response.parse()
        assert_matches_type(ObjectCreateResponse, object_, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Objective) -> None:
        with client.objects.with_streaming_response.create(
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = response.parse()
            assert_matches_type(ObjectCreateResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update(self, client: Objective) -> None:
        object_ = client.objects.update(
            object_id="obj_123",
            body={},
        )
        assert_matches_type(ObjectUpdateResponse, object_, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Objective) -> None:
        response = client.objects.with_raw_response.update(
            object_id="obj_123",
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = response.parse()
        assert_matches_type(ObjectUpdateResponse, object_, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Objective) -> None:
        with client.objects.with_streaming_response.update(
            object_id="obj_123",
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = response.parse()
            assert_matches_type(ObjectUpdateResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Objective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `object_id` but received ''"):
            client.objects.with_raw_response.update(
                object_id="",
                body={},
            )

    @parametrize
    def test_method_list(self, client: Objective) -> None:
        object_ = client.objects.list()
        assert_matches_type(ObjectListResponse, object_, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Objective) -> None:
        object_ = client.objects.list(
            cursor="cursor",
            include_metadata=True,
            include_object=True,
            limit=0,
        )
        assert_matches_type(ObjectListResponse, object_, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Objective) -> None:
        response = client.objects.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = response.parse()
        assert_matches_type(ObjectListResponse, object_, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Objective) -> None:
        with client.objects.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = response.parse()
            assert_matches_type(ObjectListResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Objective) -> None:
        object_ = client.objects.delete(
            "obj_123",
        )
        assert_matches_type(ObjectDeleteResponse, object_, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Objective) -> None:
        response = client.objects.with_raw_response.delete(
            "obj_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = response.parse()
        assert_matches_type(ObjectDeleteResponse, object_, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Objective) -> None:
        with client.objects.with_streaming_response.delete(
            "obj_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = response.parse()
            assert_matches_type(ObjectDeleteResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Objective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `object_id` but received ''"):
            client.objects.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_batch(self, client: Objective) -> None:
        object_ = client.objects.batch(
            operations=[
                {
                    "method": "PUT",
                    "object": {
                        "age": "bar",
                        "name": "bar",
                    },
                    "object_id": "obj_1234",
                },
                {
                    "method": "PUT",
                    "object": {
                        "age": "bar",
                        "name": "bar",
                    },
                    "object_id": "obj_1234",
                },
                {
                    "method": "PUT",
                    "object": {
                        "age": "bar",
                        "name": "bar",
                    },
                    "object_id": "obj_1234",
                },
            ],
        )
        assert_matches_type(ObjectBatchResponse, object_, path=["response"])

    @parametrize
    def test_raw_response_batch(self, client: Objective) -> None:
        response = client.objects.with_raw_response.batch(
            operations=[
                {
                    "method": "PUT",
                    "object": {
                        "age": "bar",
                        "name": "bar",
                    },
                    "object_id": "obj_1234",
                },
                {
                    "method": "PUT",
                    "object": {
                        "age": "bar",
                        "name": "bar",
                    },
                    "object_id": "obj_1234",
                },
                {
                    "method": "PUT",
                    "object": {
                        "age": "bar",
                        "name": "bar",
                    },
                    "object_id": "obj_1234",
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = response.parse()
        assert_matches_type(ObjectBatchResponse, object_, path=["response"])

    @parametrize
    def test_streaming_response_batch(self, client: Objective) -> None:
        with client.objects.with_streaming_response.batch(
            operations=[
                {
                    "method": "PUT",
                    "object": {
                        "age": "bar",
                        "name": "bar",
                    },
                    "object_id": "obj_1234",
                },
                {
                    "method": "PUT",
                    "object": {
                        "age": "bar",
                        "name": "bar",
                    },
                    "object_id": "obj_1234",
                },
                {
                    "method": "PUT",
                    "object": {
                        "age": "bar",
                        "name": "bar",
                    },
                    "object_id": "obj_1234",
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = response.parse()
            assert_matches_type(ObjectBatchResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete_all(self, client: Objective) -> None:
        object_ = client.objects.delete_all()
        assert_matches_type(ObjectDeleteAllResponse, object_, path=["response"])

    @parametrize
    def test_raw_response_delete_all(self, client: Objective) -> None:
        response = client.objects.with_raw_response.delete_all()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = response.parse()
        assert_matches_type(ObjectDeleteAllResponse, object_, path=["response"])

    @parametrize
    def test_streaming_response_delete_all(self, client: Objective) -> None:
        with client.objects.with_streaming_response.delete_all() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = response.parse()
            assert_matches_type(ObjectDeleteAllResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_get(self, client: Objective) -> None:
        object_ = client.objects.get(
            "obj_123",
        )
        assert_matches_type(ObjectGetResponse, object_, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Objective) -> None:
        response = client.objects.with_raw_response.get(
            "obj_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = response.parse()
        assert_matches_type(ObjectGetResponse, object_, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Objective) -> None:
        with client.objects.with_streaming_response.get(
            "obj_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = response.parse()
            assert_matches_type(ObjectGetResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get(self, client: Objective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `object_id` but received ''"):
            client.objects.with_raw_response.get(
                "",
            )

    @parametrize
    def test_method_status(self, client: Objective) -> None:
        object_ = client.objects.status(
            "obj_123",
        )
        assert_matches_type(ObjectStatusResponse, object_, path=["response"])

    @parametrize
    def test_raw_response_status(self, client: Objective) -> None:
        response = client.objects.with_raw_response.status(
            "obj_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = response.parse()
        assert_matches_type(ObjectStatusResponse, object_, path=["response"])

    @parametrize
    def test_streaming_response_status(self, client: Objective) -> None:
        with client.objects.with_streaming_response.status(
            "obj_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = response.parse()
            assert_matches_type(ObjectStatusResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_status(self, client: Objective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `object_id` but received ''"):
            client.objects.with_raw_response.status(
                "",
            )


class TestAsyncObjects:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncObjective) -> None:
        object_ = await async_client.objects.create(
            body={},
        )
        assert_matches_type(ObjectCreateResponse, object_, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncObjective) -> None:
        response = await async_client.objects.with_raw_response.create(
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = await response.parse()
        assert_matches_type(ObjectCreateResponse, object_, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncObjective) -> None:
        async with async_client.objects.with_streaming_response.create(
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = await response.parse()
            assert_matches_type(ObjectCreateResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update(self, async_client: AsyncObjective) -> None:
        object_ = await async_client.objects.update(
            object_id="obj_123",
            body={},
        )
        assert_matches_type(ObjectUpdateResponse, object_, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncObjective) -> None:
        response = await async_client.objects.with_raw_response.update(
            object_id="obj_123",
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = await response.parse()
        assert_matches_type(ObjectUpdateResponse, object_, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncObjective) -> None:
        async with async_client.objects.with_streaming_response.update(
            object_id="obj_123",
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = await response.parse()
            assert_matches_type(ObjectUpdateResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncObjective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `object_id` but received ''"):
            await async_client.objects.with_raw_response.update(
                object_id="",
                body={},
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncObjective) -> None:
        object_ = await async_client.objects.list()
        assert_matches_type(ObjectListResponse, object_, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncObjective) -> None:
        object_ = await async_client.objects.list(
            cursor="cursor",
            include_metadata=True,
            include_object=True,
            limit=0,
        )
        assert_matches_type(ObjectListResponse, object_, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncObjective) -> None:
        response = await async_client.objects.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = await response.parse()
        assert_matches_type(ObjectListResponse, object_, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncObjective) -> None:
        async with async_client.objects.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = await response.parse()
            assert_matches_type(ObjectListResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncObjective) -> None:
        object_ = await async_client.objects.delete(
            "obj_123",
        )
        assert_matches_type(ObjectDeleteResponse, object_, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncObjective) -> None:
        response = await async_client.objects.with_raw_response.delete(
            "obj_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = await response.parse()
        assert_matches_type(ObjectDeleteResponse, object_, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncObjective) -> None:
        async with async_client.objects.with_streaming_response.delete(
            "obj_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = await response.parse()
            assert_matches_type(ObjectDeleteResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncObjective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `object_id` but received ''"):
            await async_client.objects.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_batch(self, async_client: AsyncObjective) -> None:
        object_ = await async_client.objects.batch(
            operations=[
                {
                    "method": "PUT",
                    "object": {
                        "age": "bar",
                        "name": "bar",
                    },
                    "object_id": "obj_1234",
                },
                {
                    "method": "PUT",
                    "object": {
                        "age": "bar",
                        "name": "bar",
                    },
                    "object_id": "obj_1234",
                },
                {
                    "method": "PUT",
                    "object": {
                        "age": "bar",
                        "name": "bar",
                    },
                    "object_id": "obj_1234",
                },
            ],
        )
        assert_matches_type(ObjectBatchResponse, object_, path=["response"])

    @parametrize
    async def test_raw_response_batch(self, async_client: AsyncObjective) -> None:
        response = await async_client.objects.with_raw_response.batch(
            operations=[
                {
                    "method": "PUT",
                    "object": {
                        "age": "bar",
                        "name": "bar",
                    },
                    "object_id": "obj_1234",
                },
                {
                    "method": "PUT",
                    "object": {
                        "age": "bar",
                        "name": "bar",
                    },
                    "object_id": "obj_1234",
                },
                {
                    "method": "PUT",
                    "object": {
                        "age": "bar",
                        "name": "bar",
                    },
                    "object_id": "obj_1234",
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = await response.parse()
        assert_matches_type(ObjectBatchResponse, object_, path=["response"])

    @parametrize
    async def test_streaming_response_batch(self, async_client: AsyncObjective) -> None:
        async with async_client.objects.with_streaming_response.batch(
            operations=[
                {
                    "method": "PUT",
                    "object": {
                        "age": "bar",
                        "name": "bar",
                    },
                    "object_id": "obj_1234",
                },
                {
                    "method": "PUT",
                    "object": {
                        "age": "bar",
                        "name": "bar",
                    },
                    "object_id": "obj_1234",
                },
                {
                    "method": "PUT",
                    "object": {
                        "age": "bar",
                        "name": "bar",
                    },
                    "object_id": "obj_1234",
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = await response.parse()
            assert_matches_type(ObjectBatchResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete_all(self, async_client: AsyncObjective) -> None:
        object_ = await async_client.objects.delete_all()
        assert_matches_type(ObjectDeleteAllResponse, object_, path=["response"])

    @parametrize
    async def test_raw_response_delete_all(self, async_client: AsyncObjective) -> None:
        response = await async_client.objects.with_raw_response.delete_all()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = await response.parse()
        assert_matches_type(ObjectDeleteAllResponse, object_, path=["response"])

    @parametrize
    async def test_streaming_response_delete_all(self, async_client: AsyncObjective) -> None:
        async with async_client.objects.with_streaming_response.delete_all() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = await response.parse()
            assert_matches_type(ObjectDeleteAllResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_get(self, async_client: AsyncObjective) -> None:
        object_ = await async_client.objects.get(
            "obj_123",
        )
        assert_matches_type(ObjectGetResponse, object_, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncObjective) -> None:
        response = await async_client.objects.with_raw_response.get(
            "obj_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = await response.parse()
        assert_matches_type(ObjectGetResponse, object_, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncObjective) -> None:
        async with async_client.objects.with_streaming_response.get(
            "obj_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = await response.parse()
            assert_matches_type(ObjectGetResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get(self, async_client: AsyncObjective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `object_id` but received ''"):
            await async_client.objects.with_raw_response.get(
                "",
            )

    @parametrize
    async def test_method_status(self, async_client: AsyncObjective) -> None:
        object_ = await async_client.objects.status(
            "obj_123",
        )
        assert_matches_type(ObjectStatusResponse, object_, path=["response"])

    @parametrize
    async def test_raw_response_status(self, async_client: AsyncObjective) -> None:
        response = await async_client.objects.with_raw_response.status(
            "obj_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = await response.parse()
        assert_matches_type(ObjectStatusResponse, object_, path=["response"])

    @parametrize
    async def test_streaming_response_status(self, async_client: AsyncObjective) -> None:
        async with async_client.objects.with_streaming_response.status(
            "obj_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = await response.parse()
            assert_matches_type(ObjectStatusResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_status(self, async_client: AsyncObjective) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `object_id` but received ''"):
            await async_client.objects.with_raw_response.status(
                "",
            )
