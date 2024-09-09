import click


@click.command(
    "update",
    short_help="Update installed platforms, packages and libraries",
    hidden=True,
)
@click.option("--core-packages", is_flag=True, help="Update only the core packages")
@click.option(
    "-c",
    "--only-check",
    is_flag=True,
    help="DEPRECATED. Please use `--dry-run` instead",
)
@click.option(
    "--dry-run", is_flag=True, help="Do not update, only check for the new versions"
)
def cli(*_, **__):
    click.secho(
        "This command is deprecated and will be removed in the next releases. \n"
        "Please use `zx pkg update` instead.",
        fg="yellow",
    )
