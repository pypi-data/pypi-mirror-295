import os
from urllib.parse import urlparse

import click

def url_validator(_ctx, _param, value):
    for url in value:
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            raise click.BadParameter(f"Invalid URL: {url}. Please provide a valid URL with scheme and domain.")
    return value


def output_validator(_ctx, _param, value):
    if not value.lower().endswith('.csv'):
        value = f"{os.path.splitext(value)[0]}.csv"
    return value

def validate_yaml_file(_ctx, _param, value):
    if value and not (value.endswith('.yml') or value.endswith('.yaml')):
        raise click.BadParameter('The cookies file must be a YML file with a .yml or .yaml extension.')
    return value