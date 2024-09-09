import os
from xia_module import Module


class GcsBackend(Module):
    module_name = "module-backend-gcs"

    def init_config(self, repo_dict: dict = None, var_dict: dict = None, **kwargs):
        """Initialization of configuration file

        Args:
            repo_dict (dict): Repository Information
            var_dict (dict): Repository Variable Dictionary
            **kwargs: Parameter to be used for configuration file changes
        """
        repo_dict, var_dict = (repo_dict or {}), (var_dict or {})
        config_file, config_dir = self.get_config_file_path()
        if "tf_bucket_name" in var_dict:
            tf_bucket_name = var_dict["tf_bucket_name"]
            tfstate_replace_dict = {
                "tf_bucket:": f"tf_bucket: {tf_bucket_name}\n",
            }
            self._config_replace(config_file, tfstate_replace_dict)
