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
  cosmos_project = var.landscape["settings"]["cosmos_project"]
  cosmos_bucket_name = var.landscape["settings"]["bucket_name"]
  cosmos_bucket_region = var.landscape["settings"]["bucket_region"]
}

locals {
  bucket_config = merge([
    for foundation, foundation_details in var.foundations : {
      (try(foundation_details.bucket_name, local.cosmos_bucket_name)) = {
        bucket_project = local.cosmos_project
        bucket_region = local.cosmos_bucket_region
      }
    } if try(foundation_details.bucket_name, local.cosmos_bucket_name) != local.cosmos_bucket_name
  ]...)
  foundation_buckets = {
    for foundation, foundation_details in var.foundations : foundation => {
      bucket_name = lookup(foundation_details, "bucket_name", local.cosmos_bucket_name)
    }
  }
}

resource "google_storage_bucket" "foundation_buckets" {
  for_each = local.bucket_config

  project = each.value["bucket_project"]
  name = each.key
  location = each.value["bucket_region"]
  uniform_bucket_level_access = true
  force_destroy = false
}

resource "github_actions_variable" "action_var_tf_bucket" {
  for_each = var.foundations

  repository       = each.value["repository_name"]
  variable_name    = "TF_BUCKET_NAME"
  value            = local.foundation_buckets[each.key]["bucket_name"]
}

resource "google_storage_bucket_iam_member" "tfstate_bucket_list" {
  for_each = var.foundations

  bucket = local.foundation_buckets[each.key]["bucket_name"]
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${var.foundation_admin_sa[each.key].email}"

  depends_on = [google_storage_bucket.foundation_buckets]
}

resource "google_storage_bucket_iam_member" "tfstate_bucket_modify" {
  for_each = var.foundations

  bucket = local.foundation_buckets[each.key]["bucket_name"]
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${var.foundation_admin_sa[each.key].email}"

  condition {
    title       = "PrefixCondition"
    description = "Grants access to objects of foundation directory"
    expression  = "resource.name.startsWith('projects/_/buckets/${local.foundation_buckets[each.key]["bucket_name"]}/objects/${each.value["parent"]}/_/${each.value["name"]}/_/')"
  }

  depends_on = [google_storage_bucket.foundation_buckets]
}