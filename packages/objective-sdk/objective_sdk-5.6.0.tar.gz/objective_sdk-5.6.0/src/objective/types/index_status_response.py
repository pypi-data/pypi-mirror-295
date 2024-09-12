# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["IndexStatusResponse", "Status"]


class Status(BaseModel):
    error: Optional[int] = FieldInfo(alias="ERROR", default=None)

    incomplete: Optional[int] = FieldInfo(alias="INCOMPLETE", default=None)

    processing: Optional[int] = FieldInfo(alias="PROCESSING", default=None)

    ready: Optional[int] = FieldInfo(alias="READY", default=None)

    uploaded: Optional[int] = FieldInfo(alias="UPLOADED", default=None)


class IndexStatusResponse(BaseModel):
    status: Status
