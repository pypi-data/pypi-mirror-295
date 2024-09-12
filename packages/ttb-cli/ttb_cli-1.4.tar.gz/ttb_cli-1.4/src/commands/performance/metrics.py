from typing import List

import click
from src.performance import PerformanceMetricsFactory
from src.utils import url_validator, output_validator, validate_yaml_file, load_urls_from_yaml


@click.command()
@click.option('--url', multiple=True, help="List of URLs to test", callback=url_validator)
@click.option('--url-file', type=click.Path(exists=True), help="Path to YAML file containing URLs", callback=validate_yaml_file)
@click.option('--output', required=True, help="Output file for Lighthouse report", callback=output_validator)
@click.option('--iterations', default=10, type=int, help="Number of iterations per URL")
@click.option('--headless', is_flag=True, default=False, help="Run headless browser")
@click.option('--concurrent', is_flag=True, default=False, help="Run tests concurrently")
@click.option('--headers_file', default=None, help="Path to JSON file containing extra headers", type=click.Path(exists=True), callback=validate_yaml_file)
@click.option('--cookies_file', default=None, help="Path to YAML file containing cookies", type=click.Path(exists=True), callback=validate_yaml_file)
def metrics(url: List[str], url_file: str, iterations: int, output: str, headless: bool, concurrent: bool, headers_file: str, cookies_file: str):
    """Run performance metrics for given URLs."""
    if url and url_file:
        raise click.UsageError("Please provide either --url or --url-file, not both.")

    if not url and not url_file:
        raise click.UsageError("Please provide either --url or --url-file.")

    urls = list(url) if url else load_urls_from_yaml(url_file)

    factory = PerformanceMetricsFactory(
        urls=urls,
        num_iterations=iterations,
        headless=headless,
        headers_file=headers_file,
        cookies_file=cookies_file
    )
    factory.run(output, concurrent=concurrent)
