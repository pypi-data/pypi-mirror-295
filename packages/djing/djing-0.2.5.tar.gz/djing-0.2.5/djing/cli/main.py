import click

from djing.cli.initializer import Initializer

from djing.cli.commands.publish import publish


@click.group()
@click.pass_context
def main(ctx):
    ctx.obj = Initializer(ctx)


main.add_command(publish, name="publish")


if __name__ == "__main__":
    main()
