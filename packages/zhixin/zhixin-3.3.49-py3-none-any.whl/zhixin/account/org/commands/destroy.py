import click

from zhixin.account.client import AccountClient


@click.command("destroy", short_help="Destroy organization")
@click.argument("orgname")
def org_destroy_cmd(orgname):
    client = AccountClient()
    click.confirm(
        "Are you sure you want to delete the `%s` organization account?\n"
        "Warning! All linked data will be permanently removed and can not be restored."
        % orgname,
        abort=True,
    )
    client.destroy_org(orgname)
    return click.secho(
        "Organization `%s` has been destroyed." % orgname,
        fg="green",
    )
