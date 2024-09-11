import json
import os

def get_cfg_dir(cli_name):
    return os.path.join(os.environ['HOME'], '.config', cli_name)

def get_cfg_file(cli_name):
    return os.path.join(get_cfg_dir(cli_name), 'config.json')

def load_cfg(cli_name):
    cfg_dir = get_cfg_dir(cli_name)
    if not os.path.exists(cfg_dir):
        os.makedirs(cfg_dir)

    cfg_path = get_cfg_file(cli_name)
    cfg = {}

    if os.path.exists(cfg_path):
        with open(cfg_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
    return cfg

def save_cfg(cli_name, cfg):
    cfg_path = get_cfg_file(cli_name)
    with open(cfg_path, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, ensure_ascii=False, indent=4)