provider "github" {
  alias = "application"
  owner = lookup(yamldecode(file("../../../config/core/github.yaml")), "github_owner", null)
}

module "gh_module_application" {
  providers = {
    github = github.application
  }

  source = "../../modules/gh-module-application"

  module_name = "gh-module-application"
  config_file = "../../../config/core/github.yaml"
  landscape = local.landscape
  applications = local.applications
  environment_dict = local.environment_dict
  app_env_config = local.app_env_config
  module_app_to_activate = local.module_app_to_activate
}
