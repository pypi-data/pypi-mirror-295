import click
from src.performance import PerformanceMetricsFactory
from src.utils import url_validator, output_validator, validate_yaml_file


@click.command()
@click.option('--url', required=True, multiple=True, help="List of URLs to test", callback=url_validator)
@click.option('--output', required=True, help="Output file for Lighthouse report", callback=output_validator)
@click.option('--iterations', default=10, type=int, help="Number of iterations per URL")
@click.option('--headless', is_flag=True, default=False, help="Run headless browser")
@click.option('--concurrent', is_flag=True, default=False, help="Run tests concurrently")
@click.option('--headers_file', default=None, help="Path to JSON file containing extra headers", type=click.Path(exists=True), callback=validate_yaml_file)
@click.option('--cookies_file', default=None, help="Path to YAML file containing cookies", type=click.Path(exists=True), callback=validate_yaml_file)
def metrics(url, iterations, output, headless, concurrent, headers_file, cookies_file):
    """Run performance metrics for given URLs."""
    factory = PerformanceMetricsFactory(
        urls=url,
        num_iterations=iterations,
        headless=headless,
        headers_file=headers_file,
        cookies_file=cookies_file
    )
    factory.run(output, concurrent=concurrent)
