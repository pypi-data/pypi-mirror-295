import os.path
from getpass import getpass

import click
import requests

from .utils import Helpers

SDK_HEADERS = {"X-Requested-With": "nyx-sdk", "content-type": "application/json"}


@click.group()
def cli():
    pass


@cli.command()
@click.argument("resolver_url", type=click.STRING)
def print_config(resolver_url: str):
    click.echo(Helpers.generate_config(resolver_url))


@cli.command()
@click.argument("resolver_url", type=click.STRING)
@click.argument("file", type=click.STRING, default=".env")
def create_env(resolver_url: str, file: str):
    with open(file, "w") as f:
        f.write(Helpers.generate_config(resolver_url))
    click.echo(f"config written to {file}")


@cli.command()
def init():
    # Check .env exists, to ask if we should override it
    exists = os.path.exists(".env")
    prompt = "Do you want to interactively create a .env? (y/N): "
    if exists:
        prompt = ".env already exists, do you wish to override it? (y/N): "
    answer = input(prompt)

    # Default is always no action
    if answer.lower() != "y":
        click.echo("Exiting with no changes")
        exit(0)

    # Get instance details, to get everything from API
    url = input("Enter Nyx URL: ").rstrip("/")
    email = input("Enter Nyx email: ")
    password = getpass("Enter Nyx password: ")

    resp = requests.post(
        url + "/api/portal/auth/login",
        json={"email": email, "password": password},
        headers=SDK_HEADERS,
    )

    # Display any failures and exit without writing
    if not resp.ok:
        click.echo(f"Unable to authorize on Nyx instance, {resp.text}")
        exit(0)

    token = resp.json()["access_token"]
    headers = SDK_HEADERS.copy()
    headers["authorization"] = f"Bearer {token}"

    # Get username
    resp = requests.get(
        url + "/api/portal/users/me",
        headers=headers,
    )

    username = resp.json()["name"]

    # Get resolver from qapi-connection
    resp = requests.get(
        url + "/api/portal/auth/qapi-connection",
        headers=headers,
    )

    resolver = resp.json()["resolver_url"]

    click.echo("Generating user/agent secrets")
    secrets = "####".join(Helpers.generate_config(resolver).split("####")[:2])
    secrets += "\n####"

    # NYX creds
    secrets += f'\nNYX_USERNAME="{username}"'
    secrets += f'\nNYX_PASSWORD="{password}"'
    secrets += f'\nNYX_EMAIL="{email}"'
    secrets += f'\nNYX_URL="{url}"'

    click.echo(
        "Our high level client (NyxLangChain) expects a configured language model, "
        "however it can be configured with other language model wrappers provided by langchain "
        "providing they support 'tool calling'. "
        "Don't forget to set the appropriate API KEY as an environment variable for the language model you wish to use."
    )

    click.echo("Writing contents to .env")
    with open(".env", "w") as f:
        f.write(secrets)


if __name__ == "__main__":
    cli()
