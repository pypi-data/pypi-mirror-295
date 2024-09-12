# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import List, Optional

from .._models import BaseModel

__all__ = ["ObjectListResponse", "Metadata", "Object", "Pagination"]


class Metadata(BaseModel):
    count: float


class Object(BaseModel):
    id: str

    date_created: str

    date_updated: str

    object: Optional[builtins.object] = None


class Pagination(BaseModel):
    next: Optional[str] = None

    prev: Optional[str] = None


class ObjectListResponse(BaseModel):
    metadata: Metadata

    objects: List[Object]

    pagination: Pagination
