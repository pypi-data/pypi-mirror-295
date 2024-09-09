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
  module_name = coalesce(var.module_name, basename(path.module))
  tfstate_config = yamldecode(file(var.config_file))
  tf_bucket_name = local.tfstate_config["default_tf_bucket"]
  cosmos_project = var.landscape["settings"]["cosmos_project"]
}

locals {
  bucket_config = lookup(local.tfstate_config, "org_buckets", {})
  reversed_bucket_config = merge(flatten([
    for name, config in local.bucket_config : [
      for path in lookup(config, "bucket_orgs", []) : zipmap([path], [name])
    ]
  ])...)
  org_bucket_dict = {
    for path, config in var.foundations : path => {
      bucket_name = try(local.reversed_bucket_config[
        reverse(sort([for k in keys(local.reversed_bucket_config) : k if startswith(path, k)]))[0]
      ], local.tf_bucket_name)
    }
  }
}

resource "google_storage_bucket" "foundation_buckets" {
  for_each = local.bucket_config

  project = lookup(each.value, "bucket_project", local.cosmos_project)
  name = each.key
  location = lookup(each.value, "bucket_region", "eu")
  uniform_bucket_level_access = true
  force_destroy = false
}

resource "github_actions_variable" "action_var_tf_bucket" {
  for_each = var.foundations

  repository       = each.value["repository_name"]
  variable_name    = "TF_BUCKET_NAME"
  value            = local.org_bucket_dict[each.key]["bucket_name"]
}

resource "google_storage_bucket_iam_member" "tfstate_bucket_list" {
  for_each = var.foundations

  bucket = local.org_bucket_dict[each.key]["bucket_name"]
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${var.foundation_admin_sa[each.key].email}"

  depends_on = [google_storage_bucket.foundation_buckets]
}

resource "google_storage_bucket_iam_member" "tfstate_bucket_modify" {
  for_each = var.foundations

  bucket = local.org_bucket_dict[each.key]["bucket_name"]
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${var.foundation_admin_sa[each.key].email}"

  condition {
    title       = "PrefixCondition"
    description = "Grants access to objects of foundation directory"
    expression  = "resource.name.startsWith('projects/_/buckets/${local.tf_bucket_name}/objects/${each.value.parent}/_/${each.value.name}/_/')"
  }

  depends_on = [google_storage_bucket.foundation_buckets]
}