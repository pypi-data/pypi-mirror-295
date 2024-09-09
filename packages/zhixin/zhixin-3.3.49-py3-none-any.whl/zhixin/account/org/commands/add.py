import click

from zhixin.account.client import AccountClient


@click.command("add", short_help="Add a new owner to organization")
@click.argument(
    "orgname",
)
@click.argument(
    "username",
)
def org_add_cmd(orgname, username):
    client = AccountClient()
    client.add_org_owner(orgname, username)
    return click.secho(
        "The new owner `%s` has been successfully added to the `%s` organization."
        % (username, orgname),
        fg="green",
    )
