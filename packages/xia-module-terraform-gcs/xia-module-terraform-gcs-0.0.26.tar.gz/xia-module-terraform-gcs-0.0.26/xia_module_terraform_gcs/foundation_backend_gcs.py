import os
from xia_module import Module
from xia_module_terraform_gcs.backend_gcs import GcsBackend


class FoundationGcsBackend(GcsBackend):
    module_name = "module-foundation-backend-gcs"
