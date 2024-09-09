provider "google" {
  alias = "fon-state-gcs"
}

provider "github" {
  alias = "fon-state-gcs"
  owner = lookup(yamldecode(file("../../../config/core/github.yaml")), "github_owner", null)
}

module "module_foundation_state_gcs" {
  providers = {
    google = google.fon-state-gcs
    github = github.fon-state-gcs
  }

  source = "../../modules/module-foundation-state-gcs"

  config_file = "../../../config/core/foundation_tfstate.yaml"
  landscape = local.landscape
  modules = local.modules
  foundations = local.foundations

  foundation_admin_sa = module.gcp_module_organization.foundation_admin_sa
  depends_on = [module.gcp_module_organization]
}
