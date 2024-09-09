import click

from zhixin.account.client import AccountClient, AccountNotAuthorized


@click.command("destroy", short_help="Destroy account")
def account_destroy_cmd():
    client = AccountClient()
    click.confirm(
        "Are you sure you want to delete the %s user account?\n"
        "Warning! All linked data will be permanently removed and can not be restored."
        % client.get_logged_username(),
        abort=True,
    )
    client.destroy_account()
    try:
        client.logout()
    except AccountNotAuthorized:
        pass
    click.secho(
        "User account has been destroyed.",
        fg="green",
    )
