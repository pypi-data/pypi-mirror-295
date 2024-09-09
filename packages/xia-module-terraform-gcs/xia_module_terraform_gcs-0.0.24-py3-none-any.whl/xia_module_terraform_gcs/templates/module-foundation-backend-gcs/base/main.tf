terraform {
  backend "gcs" {
  }
}

module "module_foundation_backend_gcs" {
  source = "../../modules/module-foundation-backend-gcs"

  config_file = "../../../config/core/tfstate.yaml"
}
