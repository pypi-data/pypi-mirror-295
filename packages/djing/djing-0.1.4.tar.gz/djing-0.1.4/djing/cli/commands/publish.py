import click

from cli.initializer import Initializer


@click.command()
@click.pass_obj
def publish(obj: Initializer):
    try:
        print("test")
    except Exception as e:
        raise click.ClickException(e)
