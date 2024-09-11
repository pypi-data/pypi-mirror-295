import click

from src.performance import LighthouseReportFactory
from src.utils import url_validator, output_validator, validate_yaml_file


@click.command()
@click.option('--url', required=True, multiple=True, help="List of URLs to test", callback=url_validator)
@click.option('--output', required=True, help="Output file for Lighthouse report", callback=output_validator)
@click.option('--headless', is_flag=True, default=False, help="Run headless browser")
@click.option('--concurrent', is_flag=True, default=False, help="Run tests concurrently")
@click.option('--preset', default='desktop', help="Lighthouse preset (desktop, mobile)", type=click.Choice(['desktop', 'mobile']))
@click.option('--headers_file', default=None, help="Path to JSON file containing extra headers", type=click.Path(exists=True), callback=validate_yaml_file)
@click.option('--cookies_file', default=None, help="Path to YAML file containing cookies", type=click.Path(exists=True), callback=validate_yaml_file)
def lighthouse_report(url, output, headless, concurrent, preset, headers_file, cookies_file):
    """Run Lighthouse report for given URLs."""
    factory = LighthouseReportFactory(
        urls=url,
        headless=headless,
        preset=preset,
        headers_file=headers_file,
        cookies_file=cookies_file
    )
    factory.run(output, concurrent=concurrent)
