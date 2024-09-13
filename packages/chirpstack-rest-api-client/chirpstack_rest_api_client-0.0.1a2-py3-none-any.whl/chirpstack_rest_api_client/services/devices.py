import logging
from typing import Optional

from pydantic import UUID4, ValidationError

from chirpstack_rest_api_client.schemas.devices import (
    CreateDeviceRequest,
    DeviceActivation,
    DeviceActivationRequest,
    GetDeviceActivationResponse,
    GetDeviceResponse,
    ListDevicesResponse,
)
from chirpstack_rest_api_client.schemas.params import DevicesQueryParams
from chirpstack_rest_api_client.services.base import ChirpstackAPIClientBase

logger = logging.getLogger(__name__)


class DeviceClient(ChirpstackAPIClientBase):
    async def create_device(self, device: CreateDeviceRequest) -> None:
        """
        Create a new device.
        """
        resp = await self.post(
            "/api/devices", json=device.model_dump(mode="json", exclude_none=True)
        )
        resp.raise_for_status()

    async def get_devices(
        self,
        application_id: UUID4,
        limit: int = 1000,
        offset: Optional[int] = None,
        search: Optional[str] = None,
        multicast_group_id: Optional[UUID4] = None,
    ) -> Optional[ListDevicesResponse]:
        """
        Get a devices list.
        """
        parms = DevicesQueryParams(
            applicationId=application_id,
            limit=limit,
            offset=offset,
            search=search,
            multicastGroupId=multicast_group_id,
        ).model_dump(exclude_none=True)
        resp = await self.get(url="/api/devices", params=parms)
        resp.raise_for_status()
        try:
            devices_model = ListDevicesResponse.model_validate(resp.json())
            return devices_model
        except ValidationError:
            logger.error(
                f"Invalid list devices response from ChirpStack: {resp.json()}"
            )

    async def get_device_by_id(self, device_id: str) -> Optional[GetDeviceResponse]:
        """
        Get a device by id.
        """
        resp = await self.get(f"/api/devices/{device_id}")
        resp.raise_for_status()
        try:
            device_model = GetDeviceResponse.model_validate(resp.json())
            return device_model
        except ValidationError:
            logger.error(f"Invalid device response from ChirpStack: {resp.json()}")

    async def delete_device_by_id(self, device_id: str) -> None:
        """
        Delete a device by id.
        """
        resp = await self.delete(f"/api/devices/{device_id}")
        resp.raise_for_status()
        logger.info(f"Device {device_id} deleted")

    async def activate_device_by_id(
        self, deveui: str, device_activation: DeviceActivationRequest
    ) -> None:
        """
        Activate a device by id.
        """
        resp = await self.post(
            f"/api/devices/{deveui}/activate",
            json=device_activation.model_dump(mode="json", exclude_none=True),
        )
        resp.raise_for_status()
        logger.info(f"Device {deveui} activated")

    async def delete_device_activation(self, device_id: str) -> None:
        """
        Delete a device activation by id.
        """
        resp = await self.delete(f"/api/devices/{device_id}/activation")
        resp.raise_for_status()
        logger.info(f"Device activation {device_id} deleted")

    async def get_device_activation(
        self, device_id: str
    ) -> Optional[GetDeviceActivationResponse]:
        """
        Get a device activation by id.
        """
        resp = await self.get(f"/api/devices/{device_id}/activation")
        resp.raise_for_status()
        # try:
        device_activation_model = GetDeviceActivationResponse.model_validate(
            resp.json()
        )
        return device_activation_model
        # except ValidationError:
        #     logger.error(
        #         f"Invalid device activation response from ChirpStack: {resp.json()}"
        #     )
