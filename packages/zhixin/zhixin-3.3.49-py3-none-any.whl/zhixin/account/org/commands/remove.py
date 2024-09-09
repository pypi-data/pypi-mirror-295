import click

from zhixin.account.client import AccountClient


@click.command("remove", short_help="Remove an owner from organization")
@click.argument(
    "orgname",
)
@click.argument(
    "username",
)
def org_remove_cmd(orgname, username):
    client = AccountClient()
    client.remove_org_owner(orgname, username)
    return click.secho(
        "The `%s` owner has been successfully removed from the `%s` organization."
        % (username, orgname),
        fg="green",
    )
