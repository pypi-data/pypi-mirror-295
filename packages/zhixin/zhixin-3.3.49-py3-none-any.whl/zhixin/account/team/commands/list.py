import json

import click
from tabulate import tabulate

from zhixin.account.client import AccountClient


@click.command("list", short_help="List teams")
@click.argument("orgname", required=False)
@click.option("--json-output", is_flag=True)
def team_list_cmd(orgname, json_output):
    client = AccountClient()
    data = {}
    if not orgname:
        for item in client.list_orgs():
            teams = client.list_teams(item.get("orgname"))
            data[item.get("orgname")] = teams
    else:
        teams = client.list_teams(orgname)
        data[orgname] = teams
    if json_output:
        return click.echo(json.dumps(data[orgname] if orgname else data))
    if not any(data.values()):
        return click.secho("You do not have any teams.", fg="yellow")
    for org_name, teams in data.items():
        for team in teams:
            click.echo()
            click.secho("%s:%s" % (org_name, team.get("name")), fg="cyan")
            click.echo("-" * len("%s:%s" % (org_name, team.get("name"))))
            table_data = []
            if team.get("description"):
                table_data.append(("Description:", team.get("description")))
            table_data.append(
                (
                    "Members:",
                    (
                        ", ".join(
                            (member.get("username") for member in team.get("members"))
                        )
                        if team.get("members")
                        else "-"
                    ),
                )
            )
            click.echo(tabulate(table_data, tablefmt="plain"))
    return click.echo()
