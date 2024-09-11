#  Copyright (c) 2024.  - All Rights Reserved
#  You may use, distribute and modify this code under the terms of the TAMM license, which unfortunately won't be written for another century.
#  You should have received a copy of the XYZ license with this file. If not, please contact the legal authority.
#   */

import os

BASE_DIR = os.path.dirname(os.path.join(os.path.abspath(__file__)))

import click
from src.commands.performance import lighthouse_report, metrics
from src.utils import config

@click.group()
def cli():
    """TAMM Toolbox CLI"""
    config.load_config()


cli.add_command(metrics, 'performance')
cli.add_command(lighthouse_report, 'lighthouse')

if __name__ == "__main__":
    cli()
