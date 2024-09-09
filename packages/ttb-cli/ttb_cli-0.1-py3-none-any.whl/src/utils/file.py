import os
import subprocess
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


def delete_dir(path):
    if os.path.exists(path):
        subprocess.run(['rm', '-rf', path])

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
