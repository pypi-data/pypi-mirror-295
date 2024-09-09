import click

from praetorian_cli.handlers.chariot import chariot
from praetorian_cli.handlers.cli_decorators import cli_handler


@chariot.group()
@cli_handler
def unlink(ctx):
    """ Remove a collaborator from your account """
    pass


@unlink.command('account')
@click.argument('username')
@cli_handler
def unlink_account(sdk, username):
    """ Remove a collaborator account from your account """
    sdk.accounts.delete_collaborator(username)
