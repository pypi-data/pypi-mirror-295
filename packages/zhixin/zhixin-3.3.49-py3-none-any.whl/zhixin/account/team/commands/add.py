import click

from zhixin.account.client import AccountClient
from zhixin.account.validate import validate_orgname_teamname


@click.command("add", short_help="Add a new member to team")
@click.argument(
    "orgname_teamname",
    metavar="ORGNAME:TEAMNAME",
    callback=lambda _, __, value: validate_orgname_teamname(value),
)
@click.argument(
    "username",
)
def team_add_cmd(orgname_teamname, username):
    orgname, teamname = orgname_teamname.split(":", 1)
    client = AccountClient()
    client.add_team_member(orgname, teamname, username)
    return click.secho(
        "The new member %s has been successfully added to the %s team."
        % (username, teamname),
        fg="green",
    )
