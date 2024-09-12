import logging
from typing import Optional

from pydantic import UUID4, ValidationError

from chirpstack_rest_api_client.schemas.device_profiles import (
    CreateDeviceProfileRequest,
    CreateDeviceProfileResponse,
    GetDeviceProfileResponse,
    ListDeviceProfilesResponse,
)
from chirpstack_rest_api_client.schemas.params import DeviceProfilesQueryParams
from chirpstack_rest_api_client.services.base import ChirpstackAPIClientBase

logger = logging.getLogger(__name__)


class DeviceProfileClient(ChirpstackAPIClientBase):
    async def create_device_profile(
        self, device_profile: CreateDeviceProfileRequest
    ) -> Optional[CreateDeviceProfileResponse]:
        """
        Create a new device profile.
        """
        resp = await self.post(
            "/api/device-profiles",
            json=device_profile.model_dump(mode="json", exclude_none=True),
        )
        resp.raise_for_status()
        try:
            device_profile_model = CreateDeviceProfileResponse.model_validate(
                resp.json()
            )
            return device_profile_model
        except ValidationError:
            logger.error(
                f"Invalid create device profile response from ChirpStack: {resp.json()}"
            )

    async def get_device_profiles(
        self,
        tenant_id: UUID4,
        limit: int = 1000,
        offset: Optional[int] = None,
        search: Optional[str] = None,
    ) -> Optional[ListDeviceProfilesResponse]:
        """
        Get a device profiles list.
        """
        params = DeviceProfilesQueryParams(
            limit=limit, offset=offset, search=search, tenantId=tenant_id
        ).model_dump(exclude_none=True)
        resp = await self.get(url="/api/device-profiles", params=params)
        resp.raise_for_status()
        try:
            device_profiles_model = ListDeviceProfilesResponse.model_validate(
                resp.json()
            )
            return device_profiles_model
        except ValidationError:
            logger.error(
                f"Invalid list device profiles response from ChirpStack: {resp.json()}"
            )

    async def get_device_profile_by_id(
        self, device_profile_id: UUID4
    ) -> Optional[GetDeviceProfileResponse]:
        """
        Get a device profile by id.
        """
        resp = await self.get(f"/api/device-profiles/{device_profile_id}")
        resp.raise_for_status()
        try:
            device_profile_model = GetDeviceProfileResponse.model_validate(resp.json())
            return device_profile_model
        except ValidationError:
            logger.error(
                f"Invalid device profile response from ChirpStack: {resp.json()}"
            )

    async def delete_device_profile_by_id(self, device_profile_id: UUID4) -> None:
        """
        Delete a device profile by id.
        """
        resp = await self.delete(f"/api/device-profiles/{device_profile_id}")
        resp.raise_for_status()
        logger.info(f"Device profile {device_profile_id} deleted")
