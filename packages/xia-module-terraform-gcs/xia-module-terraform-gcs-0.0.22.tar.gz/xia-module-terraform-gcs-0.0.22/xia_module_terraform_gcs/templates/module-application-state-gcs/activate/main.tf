terraform {
  required_providers {
    github = {
      source  = "integrations/github"
    }
    google = {
      source  = "hashicorp/google"
    }
  }
}

locals {
  module_name = coalesce(var.module_name, substr(basename(path.module), 9, length(basename(path.module)) - 9))
  tfstate_config = yamldecode(file(var.config_file))
  tf_bucket_name = local.tfstate_config["tf_bucket"]
}

resource "google_storage_bucket_iam_member" "tfstate_bucket_admin" {
  for_each = var.foundations
  bucket = local.tf_bucket_name
  role   = "roles/storage.admin"
  member = "serviceAccount:${var.foundation_admin_sa[each.key].email}"
}