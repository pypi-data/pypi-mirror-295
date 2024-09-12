import logging
from typing import Optional

from pydantic import UUID4, ValidationError

from chirpstack_rest_api_client.schemas.params import GatewaysQueryParams
from chirpstack_rest_api_client.schemas.gateways import (
    CreateGatewayRequest,
    GetGatewayResponse,
    ListGatewaysResponse,
)
from chirpstack_rest_api_client.services.base import ChirpstackAPIClientBase

logger = logging.getLogger(__name__)


class GatewayClient(ChirpstackAPIClientBase):
    async def create_gateway(self, gateway: CreateGatewayRequest) -> None:
        """
        Create a new gateway.
        """
        resp = await self.post(
            "/api/gateways", json=gateway.model_dump(mode="json", exclude_none=True)
        )
        resp.raise_for_status()

    async def get_gateways(self, limit: int = 1000, offset: Optional[int] = None,
    search: Optional[str] = None, tenant_id: Optional[UUID4] = None, multicast_group: Optional[UUID4] = None) -> Optional[ListGatewaysResponse]:
        """
        Get a gateways list.
        """
        params = GatewaysQueryParams(
            limit=limit,
            offset=offset,
            search=search,
            tenantId=tenant_id,
            multicastGroupId=multicast_group,
        ).model_dump(exclude_none=True)
        resp = await self.get(url="/api/gateways",params=params)
        resp.raise_for_status()
        try:
            gateways_model = ListGatewaysResponse.model_validate(resp.json())
            return gateways_model
        except ValidationError:
            logger.error(
                f"Invalid list gateway response from ChirpStack: {resp.json()}"
            )

    async def get_gateway_by_id(self, gateway_id: str) -> Optional[GetGatewayResponse]:
        """
        Get a gateway by id.
        """
        resp = await self.get(f"/api/gateways/{gateway_id}")
        resp.raise_for_status()
        #try:
        gateway_model = GetGatewayResponse.model_validate(resp.json())
        return gateway_model
       # except ValidationError:
         #   logger.error(f"Invalid gateway response from ChirpStack: {resp.json()}")

    async def delete_gateway_by_id(self, gateway_id: UUID4) -> None:
        """
        Delete a gateway by id.
        """
        resp = await self.delete(f"/api/gateways/{gateway_id}")
        resp.raise_for_status()
        logger.info(f"Gateway {gateway_id} deleted")
