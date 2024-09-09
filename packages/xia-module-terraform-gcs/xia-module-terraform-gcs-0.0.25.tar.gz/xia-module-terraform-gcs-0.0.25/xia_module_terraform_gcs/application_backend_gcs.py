import os
from xia_module import Module
from xia_module_terraform_gcs.backend_gcs import GcsBackend


class ApplicationGcsBackend(GcsBackend):
    module_name = "module-application-backend-gcs"
