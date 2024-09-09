import click

from zhixin.account.client import AccountClient


@click.command("logout", short_help="Log out of ZhiXin Account")
def account_logout_cmd():
    client = AccountClient()
    client.logout()
    click.secho("Successfully logged out!", fg="green")
