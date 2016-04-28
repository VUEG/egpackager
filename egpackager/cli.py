#!/usr/bin/env python

import click
import sys

from egpackager.registry import RegistryManager

@click.group()
@click.pass_context
def cli(ctx):
    '''

    '''
    ctx.obj = {}
    ctx.obj['MANAGER'] = RegistryManager()


@cli.command()
@click.pass_context
@click.option('--type', type=click.Choice(['gspread']), help='type of data source')
@click.option('--uri', default='', help='URI to the data source')
@click.option('--credentials', default='', help='path to Google Drive API credentials JSON file')
@click.argument('raster', nargs=1)
def create_metadata(ctx, uri, type, credentials, raster):
    if type == 'gspread':
        try:
            if uri == '':
                raise click.ClickException('For Google spreadsheets, an URI must be provided')
            elif credentials == '':
                raise click.ClickException('For Google spreadsheets, a path to Google Drive API credentials JSON file must be provided')
            else:
                ctx.obj['MANAGER'].add_gpsread_datasource(uri, credentials)
        except click.ClickException as e:
            e.show()
        except FileNotFoundError  as e:
            click.echo(click.style('File {0} not found'.format(credentials), fg='red'))

@cli.command()
def list():
    click.echo(click.style('Dropped the database', fg='red'))

if __name__ == '__main__':
    cli()
