import click

from praetorian_cli.handlers.chariot import chariot
from praetorian_cli.handlers.cli_decorators import cli_handler


@chariot.group()
@cli_handler
def delete(ctx):
    """Delete a resource from Chariot"""
    pass


@delete.command('asset')
@click.argument('key', required=True)
@cli_handler
def asset(sdk, key):
    """
    Delete an asset

    KEY is the key of an existing asset

    \b
    Example usages:
        - praetorian chariot delete asset '#asset#example.com#1.2.3.4'
    """
    sdk.assets.delete(key)


@delete.command('risk')
@click.argument('key', required=True)
@click.option('-c', '--comment', default='', help='Optional comment for the delete')
@cli_handler
def risk(sdk, key, comment):
    """ Delete a risk """
    sdk.risks.delete(key, comment)


@delete.command('attribute')
@click.argument('key', required=True)
@cli_handler
def attribute(sdk, key):
    """ Delete an attribute """
    sdk.attributes.delete(key)


@delete.command('webhook')
@cli_handler
def webhook(sdk):
    """ Delete webhook """
    if sdk.webhook.get_record():
        sdk.webhook.delete()
        click.echo("Webhook successfully deleted.")
    else:
        click.echo("No webhook previously exists.")


# Special command for deleting your account and all related information.
@chariot.command('purge')
@cli_handler
def purge(controller):
    """Delete account and all related information"""
    if click.confirm("This will delete all your data and revoke access, are you sure?", default=False):
        controller.purge()
    else:
        click.echo("Operation cancelled")
        return
    click.echo("Account deleted successfully")
