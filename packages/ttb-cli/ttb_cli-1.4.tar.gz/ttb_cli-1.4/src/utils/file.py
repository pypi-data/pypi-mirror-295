import os
import shutil
import time
from typing import List

import yaml

from .config import config

def create_tmp_dir():
    if not os.path.exists(config.tmp_dir):
        os.makedirs(config.tmp_dir)

def create_tmp_dir_(path):
    if not os.path.exists(config.tmp_dir):
        os.makedirs(config.tmp_dir)

    tmp_dir_path = os.path.join(config.tmp_dir, path)
    if not os.path.exists(tmp_dir_path):
        os.makedirs(tmp_dir_path)


def delete_dir(path, sleep_time: int = 10, retry_times: int = 3):
    if os.path.exists(path):
        # noinspection PyBroadException
        try:
            time.sleep(sleep_time)
            shutil.rmtree(path)
        except Exception as e:
            if retry_times == 0:
                raise e
            print(f"Error deleting directory: {e}, retrying...")
            delete_dir(path, sleep_time, retry_times - 1)

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)


def load_urls_from_yaml(file_path: str) -> List[str]:
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict) or 'urls' not in data or not isinstance(data['urls'], list):
        raise ValueError("Invalid YAML format. Expected a dictionary with a 'urls' key containing a list of URLs.")

    urls = data['urls']

    if not all(isinstance(url, str) for url in urls):
        raise ValueError("All URLs in the YAML file must be strings.")

    return urls


