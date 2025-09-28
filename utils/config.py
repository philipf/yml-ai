import yaml

def load_config(path: str = 'config.yml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)
