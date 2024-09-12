# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ObjectBatchResponse", "Result"]


class Result(BaseModel):
    method: Literal["PUT", "POST", "DELETE"]

    object_id: str


class ObjectBatchResponse(BaseModel):
    results: List[Result]
