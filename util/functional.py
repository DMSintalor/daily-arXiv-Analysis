from yaml import safe_load


def get_cfg():
    cfg = safe_load(open('settings.yaml'))
    return cfg
