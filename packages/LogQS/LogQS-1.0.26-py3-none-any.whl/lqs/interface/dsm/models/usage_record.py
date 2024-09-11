from uuid import UUID
from typing import Optional

from pydantic import BaseModel

from lqs.interface.dsm.models.__common__ import (
    DataResponseModel,
    TimeSeriesModel,
    PaginationModel,
    optional_field,
    Int64,
)


class UsageRecord(TimeSeriesModel):
    _repr_fields = ("timestamp", "datastore_id")

    datastore_id: UUID
    duration: Optional[Int64]
    category: Optional[str]
    usage_data: Optional[dict | list]


class UsageRecordDataResponse(DataResponseModel[UsageRecord]):
    pass


class UsageRecordListResponse(PaginationModel[UsageRecord]):
    pass


class UsageRecordCreateRequest(BaseModel):
    timestamp: Int64
    duration: Optional[Int64]
    category: Optional[str]
    usage_data: Optional[dict | list]


class UsageRecordUpdateRequest(BaseModel):
    duration: Optional[Int64] = optional_field
    category: Optional[str] = optional_field
    usage_data: Optional[dict | list] = optional_field
