from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, HttpUrl, UUID4


class Application(BaseModel):
    description: Optional[str] = None # Application description.
    id: Optional[UUID4] = None # Application ID (UUID).Note: on create this will be automatically generated.
    name: str  # Application name.
    tags: Optional[dict[str, str]] = {}
    tenantId: UUID4  # Tenant ID (UUID).


class CreateApplicationRequest(BaseModel):
    application: Application


class CreateApplicationResponse(BaseModel):
    id: UUID4


class ApplicationListItemResponse(BaseModel):
    createdAt: datetime  # Created at timestamp.
    description: str  # Application description.
    id: UUID4  # Application ID (UUID).
    name: str  # Application name.
    createdAt: datetime  # Created at timestamp.


class GetApplicationResponse(BaseModel):
    application: Application
    createdAt: datetime  # Created at timestamp.
    measurementKeys: Optional[List[str]] = []
    updatedAt: datetime  # Created at timestamp.


class ListApplicationResponse(BaseModel):
    result: List[ApplicationListItemResponse]
    totalCount: int


class EncodingEnum(str, Enum):
    json = "JSON"
    protobuf = "PROTOBUF"


class HttpIntegrationResponse(BaseModel):
    applicationId: Optional[UUID4]  # Application ID (UUID).
    encoding: EncodingEnum = EncodingEnum.json  # default: JSON:
    eventEndpointUrl: HttpUrl  # Event endpoint URL.
    # The HTTP integration will POST all events to this enpoint. The request
    # will contain a query parameters "event" containing the type of the event.
    headers: Optional[dict[str, str]] = None
    # description:
    # HTTP headers to set when making requests.
    # < * >:	string


class HttpIntegrationRequest(BaseModel):
    encoding: EncodingEnum = EncodingEnum.protobuf
    eventEndpointUrl: HttpUrl
    headers: Optional[dict[str, str]] = {}


class GetHttpIntegrationResponse(BaseModel):
    integration: HttpIntegrationResponse


class CreateHttpIntegrationRequest(BaseModel):
    integration: HttpIntegrationRequest
