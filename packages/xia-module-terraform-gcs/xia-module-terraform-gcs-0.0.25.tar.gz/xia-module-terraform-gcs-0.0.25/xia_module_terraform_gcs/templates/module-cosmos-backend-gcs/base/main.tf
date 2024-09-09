terraform {
  backend "gcs" {
  }
}

module "module_cosmos_backend_gcs" {
  source = "../../modules/module-cosmos-backend-gcs"

  config_file = "../../../config/core/tfstate.yaml"
}