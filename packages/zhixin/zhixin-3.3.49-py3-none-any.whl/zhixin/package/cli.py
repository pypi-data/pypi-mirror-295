import click

from zhixin.package.commands.exec import package_exec_cmd
from zhixin.package.commands.install import package_install_cmd
from zhixin.package.commands.list import package_list_cmd
from zhixin.package.commands.outdated import package_outdated_cmd
from zhixin.package.commands.pack import package_pack_cmd
from zhixin.package.commands.publish import package_publish_cmd
from zhixin.package.commands.search import package_search_cmd
from zhixin.package.commands.show import package_show_cmd
from zhixin.package.commands.uninstall import package_uninstall_cmd
from zhixin.package.commands.unpublish import package_unpublish_cmd
from zhixin.package.commands.update import package_update_cmd


@click.group(
    "pkg",
    commands=[
        package_exec_cmd,
        package_install_cmd,
        package_list_cmd,
        package_outdated_cmd,
        package_pack_cmd,
        package_publish_cmd,
        package_search_cmd,
        package_show_cmd,
        package_uninstall_cmd,
        package_unpublish_cmd,
        package_update_cmd,
    ],
    short_help="Unified Package Manager",
)
def cli():
    pass
