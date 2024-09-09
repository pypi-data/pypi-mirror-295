import click

from zhixin.account.client import AccountClient
from zhixin.account.validate import (
    validate_email,
    validate_password,
    validate_username,
)


@click.command("register", short_help="Create new ZhiXin Account")
@click.option(
    "-u",
    "--username",
    prompt=True,
    callback=lambda _, __, value: validate_username(value),
)
@click.option(
    "-e", "--email", prompt=True, callback=lambda _, __, value: validate_email(value)
)
@click.option(
    "-p",
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    callback=lambda _, __, value: validate_password(value),
)
@click.option("--firstname", prompt=True)
@click.option("--lastname", prompt=True)
def account_register_cmd(username, email, password, firstname, lastname):
    client = AccountClient()
    client.registration(username, email, password, firstname, lastname)
    click.secho(
        "An account has been successfully created. "
        "Please check your mail to activate your account and verify your email address.",
        fg="green",
    )
