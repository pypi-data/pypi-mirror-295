import click

# from cli.initializer import Initializer

# from cli.commands.login import login
# from cli.commands.run import run
# from cli.commands.deploy import deploy


@click.group()
@click.pass_context
def run(ctx):
    print("hello")
    # ctx.obj = Initializer(ctx)


# run.add_command(login, name="login")
# run.add_command(run, name="run")
# run.add_command(deploy, name="deploy")


if __name__ == "__main__":
    run()
