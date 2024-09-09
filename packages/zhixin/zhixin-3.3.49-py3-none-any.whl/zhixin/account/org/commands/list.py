import json

import click
from tabulate import tabulate

from zhixin.account.client import AccountClient


@click.command("list", short_help="List organizations and their members")
@click.option("--json-output", is_flag=True)
def org_list_cmd(json_output):
    client = AccountClient()
    orgs = client.list_orgs()
    if json_output:
        return click.echo(json.dumps(orgs))
    if not orgs:
        return click.echo("You do not have any organization")
    for org in orgs:
        click.echo()
        click.secho(org.get("orgname"), fg="cyan")
        click.echo("-" * len(org.get("orgname")))
        data = []
        if org.get("displayname"):
            data.append(("Display Name:", org.get("displayname")))
        if org.get("email"):
            data.append(("Email:", org.get("email")))
        data.append(
            (
                "Owners:",
                ", ".join((owner.get("username") for owner in org.get("owners"))),
            )
        )
        click.echo(tabulate(data, tablefmt="plain"))
    return click.echo()
