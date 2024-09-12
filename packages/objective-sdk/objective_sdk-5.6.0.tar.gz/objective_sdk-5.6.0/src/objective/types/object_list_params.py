# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ObjectListParams"]


class ObjectListParams(TypedDict, total=False):
    cursor: str

    include_metadata: bool

    include_object: bool

    limit: float
