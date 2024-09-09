import click

from zhixin.account.client import AccountClient
from zhixin.account.validate import validate_email, validate_orgname


@click.command("create", short_help="Create a new organization")
@click.argument(
    "orgname",
    callback=lambda _, __, value: validate_orgname(value),
)
@click.option(
    "--email", callback=lambda _, __, value: validate_email(value) if value else value
)
@click.option(
    "--displayname",
)
def org_create_cmd(orgname, email, displayname):
    client = AccountClient()
    client.create_org(orgname, email, displayname)
    return click.secho(
        "The organization `%s` has been successfully created." % orgname,
        fg="green",
    )
