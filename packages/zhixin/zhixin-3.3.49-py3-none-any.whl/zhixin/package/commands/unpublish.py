import click

from zhixin.account.client import AccountClient
from zhixin.package.meta import PackageSpec, PackageType
from zhixin.registry.client import RegistryClient


@click.command("unpublish", short_help="Remove a pushed package from the registry")
@click.argument(
    "package", required=True, metavar="[<organization>/]<pkgname>[@<version>]"
)
@click.option(
    "--type",
    type=click.Choice(list(PackageType.items().values())),
    default="library",
    help="Package type, default is set to `library`",
)
@click.option(
    "--undo",
    is_flag=True,
    help="Undo a remove, putting a version back into the registry",
)
def package_unpublish_cmd(package, type, undo):  # pylint: disable=redefined-builtin
    spec = PackageSpec(package)
    response = RegistryClient().unpublish_package(
        owner=spec.owner or AccountClient().get_logged_username(),
        type=type,
        name=spec.name,
        version=str(spec.requirements),
        undo=undo,
    )
    click.secho(response.get("message"), fg="green")
