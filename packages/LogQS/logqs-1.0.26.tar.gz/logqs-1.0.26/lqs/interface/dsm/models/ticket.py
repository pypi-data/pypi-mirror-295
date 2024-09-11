from enum import Enum

from pydantic import BaseModel

from lqs.interface.dsm.models.__common__ import (
    DataResponseModel,
)


class TicketType(str, Enum):
    question = "Question"
    software_issue = "Software Issue"
    feature_request = "Feature Request"
    billing = "Billing"
    documentation = "Documentation"
    other = "Other"


class Ticket(BaseModel):
    subject: str
    type: TicketType
    description: str
    email: str
    priority: int
    status: int


class TicketDataResponse(DataResponseModel[Ticket]):
    pass


class TicketCreateRequest(BaseModel):
    type: TicketType
    description: str
    email: str
