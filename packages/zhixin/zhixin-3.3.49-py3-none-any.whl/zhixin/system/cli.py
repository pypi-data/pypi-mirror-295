import click

from zhixin.system.commands.completion import system_completion_cmd
from zhixin.system.commands.info import system_info_cmd
from zhixin.system.commands.prune import system_prune_cmd


@click.group(
    "system",
    commands=[
        system_completion_cmd,
        system_info_cmd,
        system_prune_cmd,
    ],
    short_help="Miscellaneous system commands",
)
def cli():
    pass
