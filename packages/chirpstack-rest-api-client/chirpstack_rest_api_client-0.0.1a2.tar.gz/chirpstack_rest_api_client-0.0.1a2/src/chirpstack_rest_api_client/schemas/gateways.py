from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, UUID4


class CommonLocationSourceEnum(str, Enum):
    unknow = "UNKNOWN"
    gps = "GPS"
    config = "CONFIG"  # Manually configured.
    tdoa = "GEO_RESOLVER_TDOA"  #  Geo resolver (TDOA).
    rssi = "GEO_RESOLVER_RSSI"  # Geo resolver (RSSI).
    gnss = "GEO_RESOLVER_GNSS"  # Geo resolver (GNSS).
    wifi = "GEO_RESOLVER_WIFI"  # Geo resolver (WIFI).


class CommonLocation(BaseModel):
    accuracy: float = 0.0  # Accuracy.
    altitude: float = 0.0  # Altitude.
    latitude: float = 0.0  # Latitude.
    longitude: float = 0.0  # Longitude.
    source: CommonLocationSourceEnum = CommonLocationSourceEnum.gps


class GatewayStatesEnum(str, Enum):
    never_seen = "NEVER_SEEN"  # The gateway has never sent any stats.
    online = "ONLINE"  # Online
    offline = "OFFLINE"  # Offline


class GatewayListItem(BaseModel):
    createdAt: datetime  # Created at timestamp.
    description: str  # Description.
    gatewayId: str  # Gateway ID (EUI64).
    lastSeenAt: Optional[datetime]  # Last seen at timestamp.
    location: CommonLocation
    name: str  # Name.
    properties: Optional[dict[str, str]] = {}
    state: GatewayStatesEnum = GatewayStatesEnum.never_seen  # default: NEVER_SEEN
    tenantId: UUID4  # Tenant ID.
    updatedAt: datetime  # Last update timestamp.


class ListGatewaysResponse(BaseModel):
    result: List[GatewayListItem]
    totalCount: int

    def gw_list_to_dict(self) -> dict:
        """
        Convert a list of gateways objects to a dictionary with gateway id as key.
        """
        return {gw.model_dump()["gatewayId"]: gw for gw in self.result}


class Gateway(BaseModel):
    description: Optional[str] = None  # Description.
    gatewayId: str  # Gateway ID (EUI64).
    location: CommonLocation
    metadata: Optional[dict[str, str]] = {}
    name: str  # Name.
    statsInterval: int = (
        10  # Stats interval (seconds). This defines the expected interval in which the gateway sends its statistics.
    )
    tags: Optional[dict[str, str]] = {}
    tenantId: UUID4  # Tenant ID (UUID).


class CreateGatewayRequest(BaseModel):
    gateway: Gateway


class GetGatewayResponse(BaseModel):
    createdAt: datetime  # Created at timestamp.
    gateway: Gateway
    lastSeenAt: Optional[datetime]  # Last seen at timestamp.
    updatedAt: datetime  # Last update timestamp.
