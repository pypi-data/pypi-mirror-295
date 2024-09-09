terraform {
  backend "gcs" {
  }
}

module "module_application_backend_gcs" {
  source = "../../modules/module-application-backend-gcs"

  config_file = "../../../config/core/tfstate.yaml"
}