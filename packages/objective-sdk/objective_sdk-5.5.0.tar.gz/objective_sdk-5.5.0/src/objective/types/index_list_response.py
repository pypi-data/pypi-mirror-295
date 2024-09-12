# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["IndexListResponse", "Index", "Pagination"]


class Index(BaseModel):
    id: str

    created_at: str = FieldInfo(alias="createdAt")

    updated_at: str = FieldInfo(alias="updatedAt")


class Pagination(BaseModel):
    next: str

    prev: str


class IndexListResponse(BaseModel):
    indexes: List[Index]

    pagination: Pagination
