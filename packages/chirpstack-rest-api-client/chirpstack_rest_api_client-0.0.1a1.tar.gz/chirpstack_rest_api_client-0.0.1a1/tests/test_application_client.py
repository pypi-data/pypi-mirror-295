from chirpstack_rest_api_client.schemas.applications import (
    Application,
    CreateApplicationRequest,
    CreateHttpIntegrationRequest,
    HttpIntegrationRequest,
)
from chirpstack_rest_api_client.schemas.tenants import CreateTenantRequest, Tenant
from chirpstack_rest_api_client.services.applications import ApplicationClient
from chirpstack_rest_api_client.services.tenants import TenantClient


async def test_application_api(
    application_client: ApplicationClient, get_settings, get_default_tenant_id
):
    tenant_id = get_default_tenant_id
    assert tenant_id is not None
    # create application
    request_create_app = CreateApplicationRequest(
        application=Application(name="TestApplication", tenantId=tenant_id)
    )
    response_create_app = await application_client.create_application(
        request_create_app
    )
    assert response_create_app is not None
    # get application list
    response_get_app_list = await application_client.get_applications(
        tenant_id=tenant_id
    )
    assert response_get_app_list.totalCount >= 1
    # get application by id
    response_get_app = await application_client.get_application_by_id(
        response_create_app.id
    )
    assert response_get_app.application.id == response_create_app.id
    # create application integration http
    request_create_http_integration = CreateHttpIntegrationRequest(
        integration=HttpIntegrationRequest(
            eventEndpointUrl="http://localhost:8080/api/events/",
            headers=get_settings.HTTP_INTEGRATION_HEADERS,
        )
    )
    await application_client.create_application_integration_http(
        response_create_app.id, request_create_http_integration
    )
    # get application integration by id
    response_get_http_integration = (
        await application_client.get_application_integration_http(
            response_create_app.id
        )
    )
    assert (
        response_get_http_integration.integration.applicationId
        == response_create_app.id
    )
    # delete http integration by id
    await application_client.delete_application_integration_http(response_create_app.id)
    # delete application by id
    await application_client.delete_application_by_id(response_create_app.id)
