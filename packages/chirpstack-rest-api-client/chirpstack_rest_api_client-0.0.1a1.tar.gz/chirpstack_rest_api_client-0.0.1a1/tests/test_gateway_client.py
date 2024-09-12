from chirpstack_rest_api_client.schemas.gateways import (
    CommonLocation,
    CreateGatewayRequest,
    Gateway,
)
from chirpstack_rest_api_client.services.gateways import GatewayClient


async def test_gateway_api(gateway_client: GatewayClient, get_default_tenant_id):
    tenant_id = get_default_tenant_id
    # create gateway
    gateway_id = "a037a328fc0a70f7"  # MAC address of the gateway
    request_create_gateway = CreateGatewayRequest(
        gateway=Gateway(
            gatewayId=gateway_id,
            name="TestGateway",
            tenantId=tenant_id,
            location=CommonLocation(),
        )
    )
    await gateway_client.create_gateway(request_create_gateway)
    # get gateways list
    response_get_gateways = await gateway_client.get_gateways()
    assert response_get_gateways.totalCount >= 1
    # get gateway by id
    response_get_gateway = await gateway_client.get_gateway_by_id(gateway_id)
    assert response_get_gateway.gateway.gatewayId == gateway_id
    # delete gateway
    await gateway_client.delete_gateway_by_id(gateway_id)
