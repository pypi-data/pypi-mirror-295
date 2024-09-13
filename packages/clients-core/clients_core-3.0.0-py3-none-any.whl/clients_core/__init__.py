__version__ = "3.0.0"

__all__ = [
    "authentication",
    "SimpleRestClient",
    "SecuredRestClient",
    "RestClient",
    "ApiMatchClient",
    "ServiceDirectoryMatchClient",
    "GatewayMatchClient",
    "JsonPatchModel",
]


from clients_core.api_match_client import (
    ApiMatchClient,
    GatewayMatchClient,
    ServiceDirectoryMatchClient,
)
from clients_core.models import JsonPatchModel
from clients_core.rest_client import RestClient
from clients_core.secured_rest_client import SecuredRestClient
from clients_core.simple_rest_client import SimpleRestClient
