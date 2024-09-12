import random

from chirpstack_rest_api_client.schemas.devices import CreateDeviceRequest, Device, DeviceActivation, DeviceActivationRequest
from chirpstack_rest_api_client.services.applications import ApplicationClient
from chirpstack_rest_api_client.services.device_profiles import DeviceProfileClient
from chirpstack_rest_api_client.services.devices import DeviceClient


async def test_device_api(
    device_client: DeviceClient,
    application_client: ApplicationClient,
    device_profile_client: DeviceProfileClient,
    get_default_tenant_id,
    create_application,
    create_device_profile,
):
    application_id = create_application
    device_profile_id = create_device_profile
    deveui = _generate_device_eui()
    appskey = "b8d79fae97c6f74b4fc2d44c5b6cd657"
    nwskey = "ecb7d7c991eb9e0c3dab5366d806cdac"
    devaddr = "015f1a05"
    # create device
    request_create_device = CreateDeviceRequest(
        device=Device(
            name="TestDevice",
            applicationId=application_id,
            deviceProfileId=device_profile_id,
            devEui=deveui,
        )
    )
    await device_client.create_device(request_create_device)
    # get devices list
    response_get_devices = await device_client.get_devices(application_id)
    assert response_get_devices.totalCount >= 1
    # get device by id
    response_get_device = await device_client.get_device_by_id(deveui)
    assert response_get_device.device.devEui == deveui

    device_activation_request = DeviceActivationRequest(
        deviceActivation=DeviceActivation(
            devAddr=devaddr,
            appSKey=appskey,
            fNwkSIntKey=nwskey,
            nwkSEncKey=nwskey,
            sNwkSIntKey=nwskey,
        )
    )
    await device_client.activate_device_by_id(deveui=deveui, device_activation=device_activation_request)
    # get device activation status
    response_get_device_activation = await device_client.get_device_activation(
        deveui
    )
    assert response_get_device_activation.deviceActivation.devAddr == devaddr
    # delete device activation
    await device_client.delete_device_activation(deveui)
    # delete device
    await device_client.delete_device_by_id(deveui)
    # delete device profile by id
    await device_profile_client.delete_device_profile_by_id(device_profile_id)
    # delete application by id
    await application_client.delete_application_by_id(application_id)


def _generate_device_eui():
    random_bits64 = random.getrandbits(64)
    eui_bytes = random_bits64.to_bytes(8, byteorder="little")
    return eui_bytes.hex()
