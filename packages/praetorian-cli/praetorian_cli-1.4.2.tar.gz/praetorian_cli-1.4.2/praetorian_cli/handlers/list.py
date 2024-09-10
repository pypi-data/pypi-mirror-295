import click

from praetorian_cli.handlers.chariot import chariot
from praetorian_cli.handlers.cli_decorators import cli_handler, list_params, pagination
from praetorian_cli.handlers.utils import render_offset, render_list_results, pagination_size


@chariot.group()
@cli_handler
def list(ctx):
    """Get a list of entities from Chariot"""
    pass


@list.command('assets')
@list_params('DNS')
def assets(sdk, filter, details, offset, page):
    """ List assets """
    render_list_results(sdk.assets.list(filter, offset, pagination_size(page)), details)


@list.command('risks')
@list_params('DNS of the associated assets')
def risks(sdk, filter, details, offset, page):
    """ List risks """
    render_list_results(sdk.risks.list(filter, offset, pagination_size(page)), details)


@list.command('accounts')
@list_params('account email address')
def accounts(sdk, filter, details, offset, page):
    """ List accounts """
    render_list_results(sdk.accounts.list(filter, offset, pagination_size(page)), details)


@list.command('integrations')
@list_params('integration name')
def integrations(sdk, filter, details, offset, page):
    """ List integrations """
    render_list_results(sdk.integrations.list(filter, offset, pagination_size(page)), details)


@list.command('jobs')
@list_params('DNS of the job asset')
def jobs(sdk, filter, details, offset, page):
    """ List jobs """
    render_list_results(sdk.jobs.list(filter, offset, pagination_size(page)), details)


@list.command('files')
@list_params('file path')
def files(sdk, filter, details, offset, page):
    """ List files """
    render_list_results(sdk.files.list(filter, offset, pagination_size(page)), details)


@list.command('definitions')
@click.option('-f', '--filter', default="", help=f"Filter by definition name")
@pagination
@cli_handler
def definitions(sdk, filter, offset, page):
    """ List risk definitions """
    definitions, next_offset = sdk.definitions.list(filter, offset, pagination_size(page))
    click.echo('\n'.join(definitions))
    render_offset(next_offset)


@list.command('attributes')
@list_params('attribute name')
@click.option('-k', '--key', default=None, help='Filter by an asset or risk key')
def attributes(sdk, filter, key, details, offset, page):
    """List attributes\n
    You can only filter by one of the following : attribute name, asset or risk"""

    click.echo(f'filter = {filter}, details = {details}, offset = {offset}, page = {page}, key = {key}')

    render_list_results(sdk.attributes.list(filter, key, offset, pagination_size(page)), details)
