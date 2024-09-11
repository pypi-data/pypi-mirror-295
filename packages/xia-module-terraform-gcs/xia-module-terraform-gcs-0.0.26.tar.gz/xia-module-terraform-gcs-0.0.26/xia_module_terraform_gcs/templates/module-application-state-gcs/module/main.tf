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
  landscape = var.landscape
  applications = var.applications
  settings = lookup(local.landscape, "settings", {})
  cosmos_name = local.settings["cosmos_name"]
  realm_name = local.settings["realm_name"]
  foundation_name = local.settings["foundation_name"]
  tf_bucket_name = local.tfstate_config["tf_bucket"]
  environment_dict = var.environment_dict

  app_to_activate = lookup(var.module_app_to_activate, local.module_name, [])
  app_tf_config = { for app in local.app_to_activate : app => local.tf_bucket_name }
  app_configuration = { for k, v in var.app_env_config : k => v if contains(local.app_to_activate, v["app_name"]) }
}


resource "github_actions_variable" "action_var_tf_bucket" {
  for_each = local.app_tf_config

  repository       = local.applications[each.key]["repository_name"]
  variable_name    = "TF_BUCKET_NAME"
  value            = each.value
}

resource "google_storage_bucket_iam_member" "tfstate_bucket_list" {
  for_each = local.app_configuration
  bucket = local.tf_bucket_name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${var.github_provider_sa_dict[each.key].email}"
}

resource "google_storage_bucket_iam_member" "tfstate_bucket_modify" {
  for_each = local.app_configuration
  bucket = local.tf_bucket_name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${var.github_provider_sa_dict[each.key].email}"

  condition {
    title       = "PrefixCondition"
    description = "Grants access to objects in a specific directory"
    expression  = "resource.name.startsWith('projects/_/buckets/${local.tf_bucket_name}/objects/${local.realm_name}/_/${local.foundation_name}/${each.value["app_name"]}/${each.value["env_name"]}/')"
  }
}
