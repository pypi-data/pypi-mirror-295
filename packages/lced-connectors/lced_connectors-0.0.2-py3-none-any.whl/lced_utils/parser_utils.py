import os
import yaml
from yaml import CLoader
from lced_utils.encryption_utils import decrypt_file
from lced_utils.file_utils import get_file_extensions


def config_parser(env=None, path=None):
    project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not path:
        config_tag = "config"
        config_path = os.path.join(project_root_path, config_tag)
        file_extensions = get_file_extensions(config_path)
        if ".yaml" in file_extensions:
            suffix = "yaml"
        else:
            suffix = "bin"
        conf_file_name = (
            f"{config_tag}_{env}.{suffix}" if env else f"{config_tag}.{suffix}"
        )
        path = os.path.join(config_path, conf_file_name)
    if os.path.splitext(path)[-1] == ".yaml":
        with open(path, mode="r", encoding="utf-8") as f:
            return yaml.load(f, Loader=CLoader)
    elif os.path.splitext(path)[-1] == ".bin":
        key_path = os.path.join(project_root_path, "private", "config_key.bin")
        yaml_str = decrypt_file(path, key_path)
        return yaml.safe_load(yaml_str)
    else:
        return {}


if __name__ == "__main__":
    result = config_parser("../config/config.yaml")
    print(result)
