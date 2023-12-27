from yaml import safe_load


def get_cfg():
    cfg = safe_load(open('settings.yaml'))
    return cfg


def cleanup(doms, strip=True):
    if strip:
        return ''.join([it.strip() for it in doms]).strip()
    else:
        return ''.join(doms).strip()
