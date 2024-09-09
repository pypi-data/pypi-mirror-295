import click

from zhixin.account.client import AccountClient
from zhixin.account.validate import validate_orgname_teamname, validate_teamname


@click.command("update", short_help="Update team")
@click.argument(
    "orgname_teamname",
    metavar="ORGNAME:TEAMNAME",
    callback=lambda _, __, value: validate_orgname_teamname(value),
)
@click.option(
    "--name",
    callback=lambda _, __, value: validate_teamname(value) if value else value,
    help="A new team name",
)
@click.option(
    "--description",
)
def team_update_cmd(orgname_teamname, **kwargs):
    orgname, teamname = orgname_teamname.split(":", 1)
    client = AccountClient()
    team = client.get_team(orgname, teamname)
    new_team = {
        key: value if value is not None else team[key] for key, value in kwargs.items()
    }
    if not any(kwargs.values()):
        for key in kwargs:
            new_team[key] = click.prompt(key.capitalize(), default=team[key])
            if key == "name":
                validate_teamname(new_team[key])
    client.update_team(orgname, teamname, new_team)
    return click.secho(
        "The team %s has been successfully updated." % teamname,
        fg="green",
    )
