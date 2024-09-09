import click

from zhixin.account.client import AccountClient
from zhixin.account.validate import validate_orgname_teamname


@click.command("create", short_help="Create a new team")
@click.argument(
    "orgname_teamname",
    metavar="ORGNAME:TEAMNAME",
    callback=lambda _, __, value: validate_orgname_teamname(value),
)
@click.option(
    "--description",
)
def team_create_cmd(orgname_teamname, description):
    orgname, teamname = orgname_teamname.split(":", 1)
    client = AccountClient()
    client.create_team(orgname, teamname, description)
    return click.secho(
        "The team %s has been successfully created." % teamname,
        fg="green",
    )
