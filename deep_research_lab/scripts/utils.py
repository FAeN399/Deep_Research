import yaml


def load_yaml(cfg_path):
    """Load a YAML configuration file."""
    with open(cfg_path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)
