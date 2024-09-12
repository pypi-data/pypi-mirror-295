import logging
from typing import Optional

from httpx import options
from pydantic import UUID4, ValidationError

from chirpstack_rest_api_client.schemas.params import TenantsQueryParams
from chirpstack_rest_api_client.schemas.tenants import (
    CreateTenantResponse,
    GetTenantResponse,
    ListTenantsResponse,
    CreateTenantRequest,
)
from chirpstack_rest_api_client.services.base import ChirpstackAPIClientBase

logger = logging.getLogger(__name__)


class TenantClient(ChirpstackAPIClientBase):
    async def create_tenant(
        self, tenant: CreateTenantRequest
    ) -> Optional[CreateTenantResponse]:
        """
        Create a new tenant for the user.
        """
        resp = await self.post(
            "/api/tenants", json=tenant.model_dump(exclude_none=True)
        )
        resp.raise_for_status()
        try:
            tenant_model = CreateTenantResponse.model_validate(resp.json())
            return tenant_model
        except ValidationError:
            logger.error(
                f"Invalid create tenant response from ChirpStack: {resp.json()}"
            )

    async def get_tenants(
        self,
        limit: int = 1000,
        offset: Optional[int] = None,
        search: Optional[str] = None,
        userId: Optional[UUID4] = None,
    ) -> Optional[ListTenantsResponse]:
        """
        Get a tenants list.
        """
        params = TenantsQueryParams(
            limit=limit, offset=offset, search=search, userId=userId
        ).model_dump(exclude_none=True)
        resp = await self.get(url="/api/tenants", params=params)
        resp.raise_for_status()
        try:
            tenants_model = ListTenantsResponse.model_validate(resp.json())
            return tenants_model
        except ValidationError:
            logger.error(f"Invalid list tenant response from ChirpStack: {resp.json()}")

    async def get_tenant_by_id(self, tenant_id: UUID4) -> Optional[GetTenantResponse]:
        """
        Get a tenant by id.
        """
        resp = await self.get(f"/api/tenants/{tenant_id}")
        resp.raise_for_status()
        try:
            tenant_model = GetTenantResponse.model_validate(resp.json())
            return tenant_model
        except ValidationError:
            logger.error(f"Invalid tenant response from ChirpStack: {resp.json()}")

    async def delete_tenant_by_id(self, tenant_id: UUID4) -> None:
        """
        Delete a tenant by id.
        """
        resp = await self.delete(f"/api/tenants/{tenant_id}")
        resp.raise_for_status()
        logger.info(f"Tenant {tenant_id} deleted")
