provider "github" {
  alias = "activate-application"
  owner = lookup(yamldecode(file("../../../config/core/github.yaml")), "github_owner", null)
}

module "activate_gh_module_application" {
  providers = {
    github = github.activate-application
  }

  source = "../../modules/activate-gh-module-application"

  config_file = "../../../config/core/github.yaml"
  landscape = local.landscape
  foundations = local.foundations

}
