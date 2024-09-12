import os
from getpass import getpass

import click
import requests

from nyx_client.cli.common import SDK_CLI_DEFAULT_HEADERS
from nyx_client.utils import Helpers


def init_env(filename: str = ".env"):
    if filename != "-":
        # Check .env exists, to ask if we should override it
        if os.path.exists(filename):
            prompt = f"'{filename}' already exists, do you wish to override it? (y/N): "
        else:
            prompt = f"Do you want to interactively create '{filename}'? (y/N): "
        # Default is always no action
        if input(prompt).lower() != "y":
            click.echo("Exiting with no changes")
            exit(0)

    # Get instance details, to get everything from API
    url = input("Enter Nyx URL: ").rstrip("/")
    email = input("Enter Nyx email: ")
    password = getpass("Enter Nyx password: ")

    headers = SDK_CLI_DEFAULT_HEADERS.copy()

    resp = requests.post(
        url + "/api/portal/auth/login",
        json={"email": email, "password": password},
        headers=headers,
    )

    # Display any failures and exit without writing
    if not resp.ok:
        click.echo(f"Unable to authorize on Nyx instance, {resp.text}")
        exit(1)

    token = resp.json()["access_token"]
    headers["authorization"] = f"Bearer {token}"

    # Get username
    resp = requests.get(
        url + "/api/portal/users/me",
        headers=headers,
    )
    if not resp.ok:
        click.echo(f"Unable to retrieve Nyx user details, {resp.text}")
        exit(1)

    username = resp.json()["name"]

    # Get resolver from qapi-connection
    resp = requests.get(
        url + "/api/portal/auth/qapi-connection",
        headers=headers,
    )
    if not resp.ok:
        click.echo(f"Unable to retrieve Nyx connection information, {resp.text}")
        exit(1)

    resolver = resp.json()["resolver_url"]

    click.echo("Generating user/agent secrets")
    secrets = Helpers.generate_config(resolver)
    secrets += "\n"

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

    click.echo(f"Writing contents to {filename}")
    with click.open_file(filename, mode="w") as output:
        output.write(secrets)
