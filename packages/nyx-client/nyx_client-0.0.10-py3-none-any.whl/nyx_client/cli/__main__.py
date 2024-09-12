import click

from .init_env import init_env


@click.group()
def cli():
    """
    NYX SDK command line utilities.

    For more information please visit https://github.com/Iotic-Labs/nyx-sdk
    """


@cli.command()
@click.argument("file", type=click.Path(writable=True, dir_okay=False), default=".env")
def init(file: str):
    """Generate an env file for the NYX client.
    Output is written to FILE (defaults to '.env' in the working directory)
    """
    return init_env(file)


if __name__ == "__main__":
    cli()
