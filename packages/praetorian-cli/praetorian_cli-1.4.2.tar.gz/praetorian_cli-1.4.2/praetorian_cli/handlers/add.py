import os.path

import click

from praetorian_cli.handlers.chariot import chariot
from praetorian_cli.handlers.cli_decorators import cli_handler
from praetorian_cli.handlers.utils import AssetPriorities
from praetorian_cli.sdk.model.globals import AddRisk


@chariot.group()
@cli_handler
def add(ctx):
    """ Add a resource to Chariot """
    pass


@add.command('asset')
@click.option('-d', '--dns', required=True, help='The DNS of the asset')
@click.option('-n', '--name', required=False, help='The name of the asset, e.g, IP address, GitHub repo URL')
@click.option('-p', '--priority', type=click.Choice(AssetPriorities.keys()),
              default='standard', help='The priority of the asset. Default: standard')
@cli_handler
def asset(sdk, name, dns, priority):
    """ Add an asset

    This command requires a DNS name for the asset. Optionally, a name can be provided
    to give the asset more specific information, such as IP address. If no name is
    provided, the DNS name will be used as the name.

    \b
    Example assets:
        - A domain name:   reddit.com
        - An IP addresses: 208.67.222.222
        - A CIDR range:    208.67.222.0/24
        - A GitHub org:    https://github.com/praetorian-inc

    \b
    Example usages:
        - praetorian chariot asset add --dns example.com
        - praetorian chariot asset add --dns example.com --name 1.2.3.4
    """
    if not name:
        name = dns
    sdk.assets.add(dns, name, AssetPriorities[priority])


@add.command('file')
@click.argument('path')
@click.option('-n', '--name', help='The file name in Chariot. Default: the full path of the uploaded file')
@cli_handler
def file(sdk, path, name):
    """
    Upload a file

    PATH is the file path in the local system
    """
    try:
        sdk.files.add(path, name)
    except Exception as e:
        click.echo(f'Unable to upload file {path}. Error: {e}', err=True)


@add.command('definition')
@click.argument('path')
@click.option('-n', '--name', help='The risk name definition. Default: the filename used')
@cli_handler
def definition(sdk, path, name):
    """
    Upload a risk definition in markdown format

    PATH:  File path in the local system
    """
    if name is None:
        name = os.path.basename(path)
    try:
        sdk.definitions.add(path, name)
    except Exception as e:
        click.echo(f'Unable to upload risk definition file {path}. Error: {e}', err=True)


@add.command('webhook')
@cli_handler
def webhook(sdk):
    """ Add an authenticated URL for posting assets and risks """
    if sdk.webhook.get_record():
        click.echo("There is an existing webhook. Delete it first before adding a new one.")
    else:
        click.echo(sdk.webhook.upsert())


@add.command('risk')
@click.argument('name', required=True)
@click.option('-a', '--asset', required=True, help='Key of an existing asset')
@click.option('-s', '--status', type=click.Choice([s.value for s in AddRisk]), required=True,
              help=f'Status of the risk')
@click.option('-comment', '--comment', default='', help='Comment for the risk')
@cli_handler
def risk(sdk, name, asset, status, comment):
    """
    Add a risk

    NAME is the name of the risk
    """
    sdk.risks.add(asset, name, status, comment)


@add.command('job')
@cli_handler
@click.argument('capability', required=True)
@click.option('-a', '--asset', required=True, help='Key of an existing asset')
def job(sdk, capability, asset):
    """ Add a job for an asset """
    sdk.jobs.add(asset, capability)


@add.command('attribute')
@click.option('-k', '--key', required=True, help='Key of an existing asset or risk')
@click.option('-n', '--name', required=True, help='Name of the attribute')
@click.option('-v', '--value', required=True, help='Value of the attribute')
@cli_handler
def attribute(sdk, key, name, value):
    """ Add an attribute for an asset or risk"""
    sdk.attributes.add(key, name, value)
