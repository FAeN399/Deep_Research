"""Utility helpers for Deep Research Lab."""
import yaml


def load_yaml(path):
    """Load a YAML file and return the contents as a dictionary."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
