# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["IndexSearchParams"]


class IndexSearchParams(TypedDict, total=False):
    filter_query: str

    limit: float

    object_fields: str

    offset: float

    query: str

    ranking_expr: str

    relevance_cutoff: str

    result_fields: str
