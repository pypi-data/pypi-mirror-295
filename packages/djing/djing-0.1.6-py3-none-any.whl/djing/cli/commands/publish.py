from pathlib import Path
import click

from djing.cli.initializer import Initializer


@click.command()
@click.pass_obj
def publish(obj: Initializer):
    try:
        print("current_working_directory", obj.cwd)
    except Exception as e:
        raise click.ClickException(e)
