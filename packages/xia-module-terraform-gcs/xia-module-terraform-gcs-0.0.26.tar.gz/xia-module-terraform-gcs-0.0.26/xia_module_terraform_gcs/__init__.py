from xia_module_terraform_gcs.cosmos_backend_gcs import CosmosGcsBackend
from xia_module_terraform_gcs.foundation_gcs import FoundationGcsState
from xia_module_terraform_gcs.foundation_backend_gcs import FoundationGcsBackend
from xia_module_terraform_gcs.application_gcs import ApplicationGcsState
from xia_module_terraform_gcs.application_backend_gcs import ApplicationGcsBackend

modules = {
    "module-cosmos-backend-gcs": "CosmosGcsBackend",
    "module-foundation-state-gcs": "FoundationGcsState",
    "module-foundation-backend-gcs": "FoundationGcsBackend",
    "module-application-state-gcs": "ApplicationGcsState",
    "module-application-backend-gcs": "ApplicationGcsBackend",
}

__all__ = [
    "CosmosGcsBackend",
    "FoundationGcsState",
    "FoundationGcsBackend",
    "ApplicationGcsState",
    "ApplicationGcsBackend"
]

__version__ = "0.0.26"
