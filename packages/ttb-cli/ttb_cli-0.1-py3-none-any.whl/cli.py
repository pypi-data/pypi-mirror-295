import click
from src.commands.performance.lighthouse import lighthouse_report
from src.commands.performance.metrics import metrics
from src.utils.config import config


@click.group()
def cli():
    """TAMM Toolbox CLI"""
    config.load_config()


cli.add_command(metrics, 'performance')
cli.add_command(lighthouse_report, 'lighthouse')

if __name__ == "__main__":
    cli()
