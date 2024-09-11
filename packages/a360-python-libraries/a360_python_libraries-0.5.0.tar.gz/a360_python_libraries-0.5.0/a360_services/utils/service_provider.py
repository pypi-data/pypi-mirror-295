import httpx
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param

from ..settings import settings
from .services_list import Services


class ServiceProvider:
    def __init__(self, client: httpx.Client, token: str = None):
        self.client = client
        self.token = token

    def fetch_data(self, service: Services, request_path: str) -> dict:
        headers = {}

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        response = self.client.get(
            f"{settings.PROJECT_HOST_SCHEME}://{service.value}/services/{service.name}{request_path}",
            headers=headers)
        response.raise_for_status()
        return response.json()


def get_service_provider(request: Request) -> ServiceProvider:
    authorization: str = request.headers.get("Authorization")
    token = None

    if authorization:
        scheme, param = get_authorization_scheme_param(authorization)
        if scheme.lower() == "bearer":
            token = param

    client = httpx.Client()
    return ServiceProvider(client=client, token=token)
