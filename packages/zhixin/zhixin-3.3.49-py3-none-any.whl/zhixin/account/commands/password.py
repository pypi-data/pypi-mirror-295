import click

from zhixin.account.client import AccountClient


@click.command("password", short_help="Change password")
@click.option("--old-password", prompt=True, hide_input=True)
@click.option("--new-password", prompt=True, hide_input=True, confirmation_prompt=True)
def account_password_cmd(old_password, new_password):
    client = AccountClient()
    client.change_password(old_password, new_password)
    click.secho("Password successfully changed!", fg="green")
