from xia_module import Module


class Foundation(Module):
    module_name = "gh-module-foundation"

    def init_config(self, repo_dict: dict = None, var_dict: dict = None, **kwargs):
        """Initialization of configuration file

        Args:
            repo_dict (dict): Repository Information
            var_dict (dict): Repository Variable Dictionary
            **kwargs: Parameter to be used for configuration file changes
        """
        repo_dict, var_dict = (repo_dict or {}), (var_dict or {})
        config_file, config_dir = self.get_config_file_path()
        if "owner" in repo_dict:
            github_owner_name = repo_dict["owner"]
            github_replace_dict = {
                "github_owner:": f"github_owner: {github_owner_name}\n",
            }
            self._config_replace(config_file, github_replace_dict)
