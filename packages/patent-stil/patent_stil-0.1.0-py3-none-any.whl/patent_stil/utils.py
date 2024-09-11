import os

import wget
from tqdm import tqdm


def downloadFile(file_url, save_path):
    def bar_custom(current, total, width=80):
        t.total = total
        t.update(current)
    if os.path.exists(save_path):
        os.remove(save_path)
    createDirs(os.path.dirname(save_path))
    with tqdm(unit='', unit_scale=True, unit_divisor=1024, miniters=1, desc="Downloading") as t:
        return wget.download(file_url, save_path, bar=bar_custom)

def createDirs(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False