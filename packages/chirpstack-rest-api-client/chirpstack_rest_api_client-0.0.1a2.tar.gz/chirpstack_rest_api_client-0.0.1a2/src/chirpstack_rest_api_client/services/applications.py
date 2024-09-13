import logging
from typing import Optional

from pydantic import UUID4, ValidationError

from chirpstack_rest_api_client.schemas.applications import (
    CreateApplicationRequest,
    CreateApplicationResponse,
    CreateHttpIntegrationRequest,
    GetApplicationResponse,
    GetHttpIntegrationResponse,
    ListApplicationResponse,
)
from chirpstack_rest_api_client.schemas.params import ApplicationsQueryParams
from chirpstack_rest_api_client.services.base import ChirpstackAPIClientBase

logger = logging.getLogger(__name__)


class ApplicationClient(ChirpstackAPIClientBase):
    async def create_application(
        self, app: CreateApplicationRequest
    ) -> Optional[CreateApplicationResponse]:
        """
        Create a new application for the user.
        """
        resp = await self.post(
            "/api/applications", json=app.model_dump(mode="json", exclude_none=True)
        )
        resp.raise_for_status()
        try:
            app_model = CreateApplicationResponse.model_validate(resp.json())
            return app_model
        except ValidationError:
            logger.error(
                f"Invalid create application response from ChirpStack: {resp.json()}"
            )

    async def get_applications(
        self,
        tenant_id: UUID4,
        limit: int = 1000,
        offset: Optional[int] = None,
        search: Optional[str] = None,
    ) -> Optional[ListApplicationResponse]:
        """
        Get a applications list.
        """
        params = ApplicationsQueryParams(
            limit=limit,
            offset=offset,
            search=search,
            tenantId=tenant_id,
        ).model_dump(exclude_none=True)
        resp = await self.get(url="/api/applications", params=params)
        resp.raise_for_status()
        try:
            apps_model = ListApplicationResponse.model_validate(resp.json())
            return apps_model
        except ValidationError:
            logger.error(
                f"Invalid list applications response from ChirpStack: {resp.json()}"
            )

    async def get_application_by_id(
        self, application_id: UUID4
    ) -> Optional[GetApplicationResponse]:
        """
        Get a application by id.
        """
        resp = await self.get(f"/api/applications/{application_id}")
        resp.raise_for_status()
        try:
            app_model = GetApplicationResponse.model_validate(resp.json())
            return app_model
        except ValidationError:
            logger.error(f"Invalid application response from ChirpStack: {resp.json()}")

    async def delete_application_by_id(self, application_id: UUID4) -> None:
        """
        Delete a application by id.
        """
        resp = await self.delete(f"/api/applications/{application_id}")
        resp.raise_for_status()
        logger.info(f"Application {application_id} deleted")

    async def get_application_integration_http(
        self, application_id: UUID4
    ) -> Optional[GetHttpIntegrationResponse]:
        """
        Get the configured HTTP integration.
        """
        resp = await self.get(f"/api/applications/{application_id}/integrations/http")
        resp.raise_for_status()
        try:
            app_model = GetHttpIntegrationResponse.model_validate(resp.json())
            return app_model
        except ValidationError:
            logger.error(
                f"Invalid application http integration response from ChirpStack: {resp.json()}"
            )

    async def create_application_integration_http(
        self, application_id: UUID4, http_integration: CreateHttpIntegrationRequest
    ) -> None:
        """
        Create a http intgration by application id.
        """
        resp = await self.post(
            f"/api/applications/{application_id}/integrations/http",
            json=http_integration.model_dump(mode="json", exclude_none=True),
        )
        resp.raise_for_status()

    async def delete_application_integration_http(self, application_id: UUID4) -> None:
        """
        Delete a http intgration by application id.
        """
        resp = await self.delete(
            f"/api/applications/{application_id}/integrations/http"
        )
        resp.raise_for_status()
        logger.info(f"Application {application_id} http integration deleted")
