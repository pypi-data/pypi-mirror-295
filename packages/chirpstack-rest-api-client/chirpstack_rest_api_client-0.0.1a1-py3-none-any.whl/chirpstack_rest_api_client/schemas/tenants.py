from typing import List, Optional
from pydantic import UUID4, BaseModel
from datetime import datetime


class Tenant(BaseModel):
    canHaveGateways: bool = True# Can the tenant create and "own" Gateways?
    description: str = ""# Tenant description.
    id: Optional[UUID4] = None # Tenant ID (UUID). Note: this value will be automatically generated on create.
    maxDeviceCount: int = 0 # Max. device count for tenant. When set to 0, the tenant can have unlimited devices.
    maxGatewayCount: int = 1000 # Same
    name: str # Tenant name,
    privateGatewaysDown: bool = False # Private gateways (downlink). 
    # If enabled, then other tenants will not be able to schedule downlink messages through the gateways of this tenant. For example, in case you
    # do want to share uplinks with other tenants (private_gateways_up=false),
    # but you want to prevent other tenants from using gateway airtime.
    privateGatewaysUp: bool = False # Private gateways (uplink).If enabled, then uplink messages will not be shared with other tenants.
    tags: dict = {}


class CreateTenantRequest(BaseModel):
    tenant: Tenant


class CreateTenantResponse(BaseModel):
    id: UUID4


class TenantListItem(BaseModel):
    canHaveGateways: bool # Can the tenant create and "own" Gateways?
    createdAt: datetime # Created at timestamp.
    id: UUID4 # Tenant ID (UUID).
    maxDeviceCount: int # Max device count. 0 = unlimited.
    maxGatewayCount: int # Max gateway count.0 = unlimited.
    name: str # Tenant name.
    privateGatewaysDown: bool # Private gateways (downlink).
    privateGatewaysUp: bool # Private gateways (uplink).
    updatedAt: datetime # Last update timestamp.


class ListTenantsResponse(BaseModel):
    result: List[TenantListItem]
    totalCount: int

class GetTenantResponse(BaseModel):
    createdAt: datetime # Created at timestamp.
    tenant: Tenant
    updatedAt: datetime # Last update timestamp.
