import click

from zhixin.account.client import AccountClient


@click.command("login", short_help="Log in to ZhiXin Account")
@click.option("-u", "--username", prompt="Username or email")
@click.option("-p", "--password", prompt=True, hide_input=True)
def account_login_cmd(username, password):
    client = AccountClient()
    client.login(username, password)
    click.secho("Successfully logged in!", fg="green")
