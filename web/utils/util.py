import os
import yaml
def get_config():
    yaml_name = os.path.join(os.path.dirname(__file__), '../config/conf.yaml')
    f = open(yaml_name)
    return yaml.load(f)