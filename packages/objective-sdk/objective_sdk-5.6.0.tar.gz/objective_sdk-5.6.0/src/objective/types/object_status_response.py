# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ObjectStatusResponse", "Index"]


class Index(BaseModel):
    id: str
    """Index ID"""

    status: Literal["UPLOADED", "PROCESSING", "READY", "ERROR", "INCOMPLETE"]
    """Index Status Type"""

    message: Optional[str] = None


class ObjectStatusResponse(BaseModel):
    indexes: List[Index]
