from httpx import AsyncClient, URL


class ChirpstackAPIClientBase(AsyncClient):
    def __init__(self, chirpstack_base_url: URL, auth_api_key: str) -> None:
        self.auth_headers = {"Authorization": f"Bearer {auth_api_key}"}
        self.chirpstack_base_url = chirpstack_base_url
        super().__init__(base_url=self.chirpstack_base_url, headers=self.auth_headers)
