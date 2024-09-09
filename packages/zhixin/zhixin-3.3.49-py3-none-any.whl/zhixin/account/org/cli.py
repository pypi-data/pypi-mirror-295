import click

from zhixin.account.org.commands.add import org_add_cmd
from zhixin.account.org.commands.create import org_create_cmd
from zhixin.account.org.commands.destroy import org_destroy_cmd
from zhixin.account.org.commands.list import org_list_cmd
from zhixin.account.org.commands.remove import org_remove_cmd
from zhixin.account.org.commands.update import org_update_cmd


@click.group(
    "account",
    commands=[
        org_add_cmd,
        org_create_cmd,
        org_destroy_cmd,
        org_list_cmd,
        org_remove_cmd,
        org_update_cmd,
    ],
    short_help="Manage organizations",
)
def cli():
    pass
