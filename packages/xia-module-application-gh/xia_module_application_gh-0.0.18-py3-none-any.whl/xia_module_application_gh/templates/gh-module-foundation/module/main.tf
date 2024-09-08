terraform {
  required_providers {
    github = {
      source  = "integrations/github"
    }
  }
}

locals {
  github_config = yamldecode(file(var.config_file))
  cosmos_name = var.landscape["settings"]["cosmos_name"]
}

resource "github_repository" "foundation-repository" {
  for_each = var.foundations

  name        = each.value["repository_name"]
  description = "Foundation: ${each.value["name"]}"

  visibility = each.value["visibility"]

  template {
    owner                = each.value["template_owner"]
    repository           = each.value["template_name"]
  }
}

resource "github_actions_variable" "action_var_cosmos_name" {
  for_each = var.foundations

  repository       = each.value["repository_name"]
  variable_name    = "COSMOS_NAME"
  value            = local.cosmos_name

  depends_on = [github_repository.foundation-repository]
}

resource "github_actions_variable" "action_var_realm_name" {
  for_each = var.foundations

  repository       = each.value["repository_name"]
  variable_name    = "REALM_NAME"
  value            = each.value["parent"]

  depends_on = [github_repository.foundation-repository]
}

resource "github_actions_variable" "action_var_foundation_name" {
  for_each = var.foundations

  repository       = each.value["repository_name"]
  variable_name    = "FOUNDATION_NAME"
  value            = each.value["name"]

  depends_on = [github_repository.foundation-repository]
}
