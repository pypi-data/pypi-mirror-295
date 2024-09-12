from typing import List

import click

from src.utils import load_urls_from_yaml


def get_urls(urls: List[str] | None, urls_file : str | None) -> List[str]:
    if urls and urls_file:
        raise click.UsageError("Please provide either --url or --urls_file, not both.")
    if not urls and not urls_file:
        raise click.UsageError("Please provide either --url or --urls_file.")

    parsed_urls = list(urls) if urls else load_urls_from_yaml(urls_file)

    return parsed_urls
