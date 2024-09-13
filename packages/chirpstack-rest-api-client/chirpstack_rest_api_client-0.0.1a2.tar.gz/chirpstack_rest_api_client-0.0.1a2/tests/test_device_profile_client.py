from chirpstack_rest_api_client.schemas.device_profiles import (
    CreateDeviceProfileRequest,
    DeviceProfile,
)
from chirpstack_rest_api_client.services.device_profiles import DeviceProfileClient


async def test_device_profile_api(
    device_profile_client: DeviceProfileClient,
    get_default_tenant_id
):
    tenant_id = get_default_tenant_id
    # create device profile
    request_create_device_profile = CreateDeviceProfileRequest(
        deviceProfile=DeviceProfile(
            name="TestDeviceProfile",
            tenantId=tenant_id,
        )
    )
    response_create_device_profile = await device_profile_client.create_device_profile(
        request_create_device_profile
    )
    device_profile_id = response_create_device_profile.id
    assert device_profile_id is not None
    # get device profiles list
    response_get_device_profiles = await device_profile_client.get_device_profiles(
        tenant_id
    )
    assert response_get_device_profiles.totalCount >= 1
    # get device profile by id
    response_get_device_profile = await device_profile_client.get_device_profile_by_id(
        device_profile_id
    )
    assert response_get_device_profile.deviceProfile.id == device_profile_id
    # delete device profile
    await device_profile_client.delete_device_profile_by_id(device_profile_id)
