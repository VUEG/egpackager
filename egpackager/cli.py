#!/usr/bin/env python

import click
import sys

from egpackager.datasources import GspreadDataSource

@click.group()
def cli():
    '''

    '''
    pass


@cli.command()
def register():
    click.echo(click.style('Initialized the database', fg='green'))


@cli.command()
def list():
    click.echo(click.style('Dropped the database', fg='red'))

if __name__ == '__main__':
    sys.exit(cli())
