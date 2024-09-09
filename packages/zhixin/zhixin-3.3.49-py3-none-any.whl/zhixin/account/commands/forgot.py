import click

from zhixin.account.client import AccountClient


@click.command("forgot", short_help="Forgot password")
@click.option("--username", prompt="Username or email")
def account_forgot_cmd(username):
    client = AccountClient()
    client.forgot_password(username)
    click.secho(
        "If this account is registered, we will send the "
        "further instructions to your email.",
        fg="green",
    )
