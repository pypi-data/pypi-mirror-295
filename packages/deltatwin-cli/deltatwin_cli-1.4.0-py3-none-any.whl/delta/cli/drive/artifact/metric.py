import json
from datetime import datetime
from typing import Union

import click

from delta.cli.utils import Utils, API
from rich.console import Console
from rich.table import Table


def format_date(date: Union[str, datetime]) -> str:
    # Parse la chaîne de date dans un objet datetime
    if type(date) is str:
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")

    # Formater l'objet datetime dans le format souhaité
    return date.strftime("%b %d, %Y, %I:%M:%S %p")


def retrieve_metric(metrics) -> dict:
    data = {}
    for metric in metrics:
        if metric['type'] == 's3':
            data['storage_used'] = metric['occupied_size']
            data['total_objects'] = metric['total_objects']
            data['last_metric_update'] = format_date(metric['metric_date'])
            return data
    data['storage_used'] = 0
    data['total_objects'] = 0
    data['last_metric_update'] = format_date(datetime.now())
    return data


@click.help_option("--help", "-h")
@click.command(
    'metric',
    short_help='It provides the amount of storage used by all user artifacts.')
@click.option(
    '--conf',
    '-c',
    type=str,
    default=None,
    help='Path to the conf file')
@click.option(
    '--format-output',
    '-f',
    type=str,
    default=None,
    help='Format of the output json/text default is text')
def get_metric(conf, format_output: str) -> None:
    """It provides the amount of storage used by all the artifact of the user

    **Example:** deltatwin drive artifact metric
    """

    metrics = API.get_metric(conf)

    data = retrieve_metric(metrics)

    if format_output is not None and format_output.lower() == 'json':
        click.echo(json.dumps(data, indent=4))
        return

    if isinstance(data, list):
        if len(data) == 0:
            click.echo(f"{Utils.log_info} No artifact found")

    table = Table()
    table.add_column('Storage used')
    table.add_column('Number of Elements')
    table.add_column('Last metric update')

    rows = (str(data['storage_used']),
            str(data['total_objects']),
            str(data['last_metric_update'])
            )
    table.add_row(*rows)
    console = Console()
    console.print(table)
