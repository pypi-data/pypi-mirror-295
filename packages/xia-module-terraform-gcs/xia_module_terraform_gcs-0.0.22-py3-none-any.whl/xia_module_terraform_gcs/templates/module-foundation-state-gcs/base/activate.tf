provider "google" {
  alias = "activate-fon-state-gcs"
}

provider "github" {
  alias = "activate-fon-state-gcs"
  owner = lookup(yamldecode(file("../../../config/core/github.yaml")), "github_owner", null)
}

module "activate_module_foundation_state_gcs" {
  providers = {
    google = google.activate-fon-state-gcs
    github = github.activate-fon-state-gcs
  }

  source = "../../modules/activate-module-foundation-state-gcs"

  landscape = local.landscape
  modules   = local.modules
}

