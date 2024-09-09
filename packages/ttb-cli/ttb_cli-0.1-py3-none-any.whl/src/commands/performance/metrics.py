import click
from src.performance import PerformanceMetricsFactory
from src.utils import url_validator, output_validator


@click.command()
@click.option('--url', required=True, multiple=True, help="List of URLs to test", callback=url_validator)
@click.option('--output', required=True, help="Output file for Lighthouse report", callback=output_validator)
@click.option('--iterations', default=10, type=int, help="Number of iterations per URL")
@click.option('--headless', is_flag=True, default=False, help="Run headless browser")
@click.option('--concurrent', is_flag=True, default=False, help="Run tests concurrently")
def metrics(url, iterations, output, headless, concurrent):
    """Run performance metrics for given URLs."""
    factory = PerformanceMetricsFactory(
        urls=url,
        num_iterations=iterations,
        headless=headless,
    )
    factory.run(output, concurrent=concurrent)
