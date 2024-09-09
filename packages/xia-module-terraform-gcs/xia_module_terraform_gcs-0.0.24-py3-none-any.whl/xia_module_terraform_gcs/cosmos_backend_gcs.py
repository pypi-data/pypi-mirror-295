import os
from xia_module import Module
from xia_module_terraform_gcs.backend_gcs import GcsBackend


class CosmosGcsBackend(GcsBackend):
    module_name = "module-cosmos-backend-gcs"
