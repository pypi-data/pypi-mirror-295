provider "github" {
  alias = "foundation"
  owner = lookup(yamldecode(file("../../../config/core/github.yaml")), "github_owner", null)
}

module "gh_module_foundation" {
  providers = {
    github = github.foundation
  }

  source = "../../modules/gh-module-foundation"

  module_name = "gh-module-foundation"
  config_file = "../../../config/core/github.yaml"
  landscape = local.landscape
  foundations = local.foundations
}
