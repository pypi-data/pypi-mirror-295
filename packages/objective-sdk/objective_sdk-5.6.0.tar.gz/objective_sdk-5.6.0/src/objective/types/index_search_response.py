# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import List, Optional

from .._models import BaseModel

__all__ = ["IndexSearchResponse", "Pagination", "PaginationNext", "Result"]


class PaginationNext(BaseModel):
    limit: float

    offset: float


class Pagination(BaseModel):
    next: PaginationNext

    page: float

    pages: float


class Result(BaseModel):
    id: str

    object: Optional[builtins.object] = None


class IndexSearchResponse(BaseModel):
    pagination: Pagination

    results: List[Result]
