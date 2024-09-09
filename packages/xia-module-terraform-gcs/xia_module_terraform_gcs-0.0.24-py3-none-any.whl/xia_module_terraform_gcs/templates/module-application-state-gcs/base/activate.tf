provider "google" {
  alias = "activate-app-state-gcs"
}

provider "github" {
  alias = "activate-app-state-gcs"
  owner = lookup(yamldecode(file("../../../config/core/github.yaml")), "github_owner", null)
}

module "activate_module_application_state_gcs" {
  providers = {
    google = google.activate-app-state-gcs
    github = github.activate-app-state-gcs
  }

  source = "../../modules/activate-module-application-state-gcs"

  config_file = "../../../config/core/tfstate.yaml"
  landscape = local.landscape
  modules   = local.modules
  foundations = local.foundations

  foundation_admin_sa = module.gcp_module_organization.foundation_admin_sa
  depends_on = [module.gcp_module_organization]
}

