from typing import List

import click

from src.performance import LighthouseReportFactory
from src.utils import url_validator, output_validator, validate_yaml_file, get_urls


@click.command()
@click.option('--url', multiple=True, help="List of URLs to test", callback=url_validator)
@click.option('--urls_file', type=click.Path(exists=True), help="Path to YAML file containing URLs", callback=validate_yaml_file)
@click.option('--output', required=True, help="Output file for Lighthouse report", callback=output_validator)
@click.option('--headless', is_flag=True, default=False, help="Run headless browser")
@click.option('--concurrent', is_flag=True, default=False, help="Run tests concurrently")
@click.option('--preset', default='desktop', help="Lighthouse preset (desktop, mobile)", type=click.Choice(['desktop', 'mobile']))
@click.option('--headers_file', default=None, help="Path to JSON file containing extra headers", type=click.Path(exists=True), callback=validate_yaml_file)
@click.option('--cookies_file', default=None, help="Path to YAML file containing cookies", type=click.Path(exists=True), callback=validate_yaml_file)
def lighthouse_report(url: List[str], urls_file: str, output: str, headless: bool, concurrent: bool, preset: str, headers_file: str, cookies_file: str):
    """Run Lighthouse report for given URLs."""

    urls = get_urls(url, urls_file)

    factory = LighthouseReportFactory(
        urls=urls,
        headless=headless,
        preset=preset,
        headers_file=headers_file,
        cookies_file=cookies_file
    )
    factory.run(output, concurrent=concurrent)
