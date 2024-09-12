import os

BASE_DIR = os.path.dirname(os.path.join(os.path.abspath(__file__)))

import click
from src.commands.performance import lighthouse_report, metrics
from src.utils import config

@click.group()
@click.pass_context
@click.version_option(package_name='ttb-cli')
def cli(ctx):
    """TAMM Toolbox CLI"""
    config.load_config()


# noinspection PyTypeChecker
cli.add_command(metrics, 'performance')
# noinspection PyTypeChecker
cli.add_command(lighthouse_report, 'lighthouse')

if __name__ == "__main__":
    cli()
