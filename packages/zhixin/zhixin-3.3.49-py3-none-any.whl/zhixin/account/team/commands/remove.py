import click

from zhixin.account.client import AccountClient
from zhixin.account.validate import validate_orgname_teamname


@click.command("remove", short_help="Remove a member from team")
@click.argument(
    "orgname_teamname",
    metavar="ORGNAME:TEAMNAME",
    callback=lambda _, __, value: validate_orgname_teamname(value),
)
@click.argument("username")
def team_remove_cmd(orgname_teamname, username):
    orgname, teamname = orgname_teamname.split(":", 1)
    client = AccountClient()
    client.remove_team_member(orgname, teamname, username)
    return click.secho(
        "The %s member has been successfully removed from the %s team."
        % (username, teamname),
        fg="green",
    )
