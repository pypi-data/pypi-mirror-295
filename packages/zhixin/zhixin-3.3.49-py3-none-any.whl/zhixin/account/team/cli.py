import click

from zhixin.account.team.commands.add import team_add_cmd
from zhixin.account.team.commands.create import team_create_cmd
from zhixin.account.team.commands.destroy import team_destroy_cmd
from zhixin.account.team.commands.list import team_list_cmd
from zhixin.account.team.commands.remove import team_remove_cmd
from zhixin.account.team.commands.update import team_update_cmd


@click.group(
    "team",
    commands=[
        team_add_cmd,
        team_create_cmd,
        team_destroy_cmd,
        team_list_cmd,
        team_remove_cmd,
        team_update_cmd,
    ],
    short_help="Manage organization teams",
)
def cli():
    pass
