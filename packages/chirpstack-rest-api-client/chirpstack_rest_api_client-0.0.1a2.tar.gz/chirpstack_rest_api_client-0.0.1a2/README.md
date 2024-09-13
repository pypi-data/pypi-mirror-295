# Chirpstack REST API client

The client for the Chirpstack REST API based on httpx and pydantic.

It contains ready-made clients with implemented methods and pydantic schemes for the following services:
- TenantService
- GatewayService
- DeviceService
- DeviceProfileService
- ApplicationService

Installing:

```
pip install chirpstack-rest-api-client
```

Usage example:

```python
from chirpstack_rest_api_client.services.tenants import TenantClient


api_key = "chirpstack_global_api_key"
base_url = "http://localhost:8090"

async def run():
    async with TenantClient(base_url, api_key) as cli:
        tenants_list = await cli.get_tenants(limit=10)
        if tenants_list.totalCount > 0:
            print(f"Tenants: {tenants_list.result}")

if __name__ == "__main__":
    import asyncio

    asyncio.run(run())        
```

### License
[Apache License, Version 2.0](https://github.com/AlKorochkin/chirpstack-rest-api-client/blob/main/LICENSE)