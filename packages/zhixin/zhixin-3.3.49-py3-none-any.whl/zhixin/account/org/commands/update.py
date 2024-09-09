import click

from zhixin.account.client import AccountClient
from zhixin.account.validate import validate_email, validate_orgname


@click.command("update", short_help="Update organization")
@click.argument("cur_orgname")
@click.option(
    "--orgname",
    callback=lambda _, __, value: validate_orgname(value) if value else value,
    help="A new orgname",
)
@click.option(
    "--email",
    callback=lambda _, __, value: validate_email(value) if value else value,
)
@click.option("--displayname")
def org_update_cmd(cur_orgname, **kwargs):
    client = AccountClient()
    org = client.get_org(cur_orgname)
    new_org = {
        key: value if value is not None else org[key] for key, value in kwargs.items()
    }
    if not any(kwargs.values()):
        for key in kwargs:
            new_org[key] = click.prompt(key.capitalize(), default=org[key])
            if key == "email":
                validate_email(new_org[key])
            if key == "orgname":
                validate_orgname(new_org[key])
    client.update_org(cur_orgname, new_org)
    return click.secho(
        "The organization `%s` has been successfully updated." % cur_orgname,
        fg="green",
    )
