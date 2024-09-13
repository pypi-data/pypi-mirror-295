from chirpstack_rest_api_client.schemas.tenants import Tenant, CreateTenantRequest

tenant_id = None

async def test_create_tenant(tenant_client):
    global tenant_id
    request = CreateTenantRequest(
        tenant = Tenant(name="TestTenant")
    )
    response = await tenant_client.create_tenant(request)
    assert response.id is not None
    tenant_id = response.id


async def test_get_tenants(tenant_client):
    list_tenants = await tenant_client.get_tenants()
    # 1 тенант всегда есть по-умолчанию
    assert list_tenants.totalCount >= 1


async  def test_get_tenant_by_id(tenant_client):
    global tenant_id
    response = await tenant_client.get_tenant_by_id(tenant_id)
    assert response.tenant.id == tenant_id


async def test_delete_tenant(tenant_client):
    global tenant_id
    await tenant_client.delete_tenant_by_id(tenant_id)
    tenant_id = None
