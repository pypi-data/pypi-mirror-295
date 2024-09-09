import json

import click

from zhixin.account.client import AccountClient


@click.command("token", short_help="Get or regenerate Authentication Token")
@click.option("-p", "--password", prompt=True, hide_input=True)
@click.option("--regenerate", is_flag=True)
@click.option("--json-output", is_flag=True)
def account_token_cmd(password, regenerate, json_output):
    client = AccountClient()
    auth_token = client.auth_token(password, regenerate)
    if json_output:
        click.echo(json.dumps({"status": "success", "result": auth_token}))
        return
    click.secho("Personal Authentication Token: %s" % auth_token, fg="green")
