from typing import Optional

from pydantic import BaseModel, UUID4


class BaseQueryParams(BaseModel):
    limit: int = 1000
    offset: Optional[int] = None
    search: Optional[str] = None


class TenantsQueryParams(BaseQueryParams):
    userId: Optional[UUID4] = None


class ApplicationsQueryParams(BaseQueryParams):
    tenantId: UUID4


class DeviceProfilesQueryParams(BaseQueryParams):
    tenantId: UUID4


class GatewaysQueryParams(BaseQueryParams):
    tenantId: Optional[UUID4] = None
    multicastGroupId: Optional[UUID4] = None


class DevicesQueryParams(BaseQueryParams):
    applicationId: Optional[UUID4] = None
    multicastGroupId: Optional[UUID4] = None