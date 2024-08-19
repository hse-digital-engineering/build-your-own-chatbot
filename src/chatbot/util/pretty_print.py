import sys

from ruamel.yaml import YAML


def pretty_print_yaml(dict: dict) -> None:
    """Pretty print a dictionary as YAML."""
    yaml = YAML()
    yaml.default_flow_style = None
    yaml.dump(dict, sys.stdout)
