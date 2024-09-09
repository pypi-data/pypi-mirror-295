import click

from zhixin.account.client import AccountClient
from zhixin.account.validate import validate_orgname_teamname


@click.command("destroy", short_help="Destroy a team")
@click.argument(
    "orgname_teamname",
    metavar="ORGNAME:TEAMNAME",
    callback=lambda _, __, value: validate_orgname_teamname(value),
)
def team_destroy_cmd(orgname_teamname):
    orgname, teamname = orgname_teamname.split(":", 1)
    click.confirm(
        click.style(
            "Are you sure you want to destroy the %s team?" % teamname, fg="yellow"
        ),
        abort=True,
    )
    client = AccountClient()
    client.destroy_team(orgname, teamname)
    return click.secho(
        "The team %s has been successfully destroyed." % teamname,
        fg="green",
    )
