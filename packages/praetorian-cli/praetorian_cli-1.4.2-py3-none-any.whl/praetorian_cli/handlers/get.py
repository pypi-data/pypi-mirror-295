import os

import click

from praetorian_cli.handlers.chariot import chariot
from praetorian_cli.handlers.cli_decorators import cli_handler
from praetorian_cli.handlers.utils import print_json


@chariot.group()
@cli_handler
def get(ctx):
    """Get resource details from Chariot"""
    pass


@get.command('asset')
@click.argument('key', required=True)
@click.option('-d', '--details', is_flag=True, help='Get attributes of the asset')
@cli_handler
def asset(sdk, key, details):
    """ Get asset details """
    print_json(sdk.assets.get(key, details))


@get.command('risk')
@click.argument('key', required=True)
@click.option('-d', '--details', is_flag=True, help='Get attributes of the risk')
@cli_handler
def risk(sdk, key, details):
    """ Get risk details """
    print_json(sdk.risks.get(key, details))


@get.command('attribute')
@click.argument('key', required=True)
@cli_handler
def attribute(sdk, key):
    """ Get asset details """
    print_json(sdk.attributes.get(key))


@get.command('account')
@click.argument('key', required=True)
@cli_handler
def account(sdk, key):
    """ Get account (collaborator or authorized master account) details """
    print_json(sdk.accounts.get(key))


@get.command('integration')
@click.argument('key', required=True)
@cli_handler
def integration(sdk, key):
    """ Get integration details """
    print_json(sdk.integrations.get(key))


@get.command('job')
@click.argument('key', required=True)
@cli_handler
def job(sdk, key):
    """ Get job details """
    print_json(sdk.jobs.get(key))


@get.command('file')
@cli_handler
@click.argument('name')
@click.option('-p', '--path', default=os.getcwd(), help="Download path. Default: save to current directory")
def file(sdk, name, path):
    """ Download a file using key or name."""
    if name.startswith('#'):
        downloaded_filepath = sdk.files.get(name.split('#')[-1], path)
    else:
        downloaded_filepath = sdk.files.get(name, path)
    print(f'Saved file at {downloaded_filepath}')


@get.command('definition')
@cli_handler
@click.argument('name')
@click.option('-path', '--path', default=os.getcwd(), help="Download path. Default: save to current directory")
def definition(sdk, name, path):
    """ Download a definition using the risk name. """
    downloaded_path = sdk.definitions.get(name, path)
    click.echo(f'Saved definition at {downloaded_path}')


@get.command('webhook')
@cli_handler
def webhook(sdk):
    """ Get the webhook URL """
    if sdk.webhook.get_record():
        click.echo(sdk.webhook.get_url())
    else:
        click.echo("No existing webhook.")
