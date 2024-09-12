# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import builtins
from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "ObjectBatchParams",
    "Operation",
    "OperationPutOperation",
    "OperationPostOperation",
    "OperationDeleteOperation",
]


class ObjectBatchParams(TypedDict, total=False):
    operations: Required[Iterable[Operation]]


class OperationPutOperation(TypedDict, total=False):
    method: Required[Literal["PUT"]]

    object: Required[Dict[str, builtins.object]]

    object_id: Required[str]


class OperationPostOperation(TypedDict, total=False):
    method: Required[Literal["POST"]]

    object: Required[Dict[str, builtins.object]]


class OperationDeleteOperation(TypedDict, total=False):
    method: Required[Literal["DELETE"]]

    object_id: Required[str]


Operation: TypeAlias = Union[OperationPutOperation, OperationPostOperation, OperationDeleteOperation]
