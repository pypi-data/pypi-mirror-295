import click

from praetorian_cli.handlers.chariot import chariot
from praetorian_cli.handlers.cli_decorators import cli_handler
from praetorian_cli.handlers.utils import render_list_results, print_json, pagination_size


@chariot.command('search')
@click.option('-t', '--term', help="Enter a search term", required=True)
@click.option('-c', '--count', is_flag=True, default=False, help="Return statistics on search")
@click.option('-d', '--details', is_flag=True, default=False, help="Show detailed information")
@click.option('-o', '--offset', default='', help='List results from an offset')
@click.option('-p', '--page', type=click.Choice(('first', 'all')), default='first',
              help="Pagination mode. 'all' pages up to 1000 pages. Default: 'first'")
@cli_handler
def search(sdk, term, count, details, offset, page):
    """ Query Chariot for arbitrary matches using the search syntax """
    if count:
        print_json(sdk.search.count(term))
    else:
        render_list_results(sdk.search.by_term(term, offset, pagination_size(page)), details)
