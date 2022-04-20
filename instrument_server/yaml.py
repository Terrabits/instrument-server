from pathlib     import Path
from ruamel.yaml import YAML


# share global parser
# rt = round trip dump
# (aka pretty-print)
yaml = YAML(typ='rt')


def load_yaml(file):
    """read yaml from file"""
    file = Path(file)
    return yaml.load(file)


def save_yaml(data, file):
    """write yaml to file"""
    file = Path(file)
    return yaml.dump(data, file)
