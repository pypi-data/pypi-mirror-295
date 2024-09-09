import click

from praetorian_cli.handlers.chariot import chariot
from praetorian_cli.handlers.cli_decorators import cli_handler


@chariot.group()
@cli_handler
def link(ctx):
    """  Add a collaborator to your account """
    pass


@link.command('account')
@cli_handler
@click.argument('username')
def link_account(sdk, username):
    """ Add a collaborator account to your account """
    sdk.accounts.add_collaborator(username)
