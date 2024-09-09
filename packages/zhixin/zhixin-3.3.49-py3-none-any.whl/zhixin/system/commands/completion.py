import click

from zhixin.system.completion import (
    ShellType,
    get_completion_install_path,
    install_completion_code,
    uninstall_completion_code,
)


@click.group("completion", short_help="Shell completion support")
def system_completion_cmd():
    pass


@system_completion_cmd.command(
    "install", short_help="Install shell completion files/code"
)
@click.argument("shell", type=click.Choice([t.value for t in ShellType]))
@click.option(
    "--path",
    type=click.Path(file_okay=True, dir_okay=False, readable=True),
    help="Custom installation path of the code to be evaluated by the shell. "
    "The standard installation path is used by default.",
)
def system_completion_install(shell, path):
    shell = ShellType(shell)
    path = path or get_completion_install_path(shell)
    install_completion_code(shell, path)
    click.echo(
        "ZhiXin CLI completion has been installed for %s shell to %s \n"
        "Please restart a current shell session."
        % (click.style(shell.name, fg="cyan"), click.style(path, fg="blue"))
    )


@system_completion_cmd.command(
    "uninstall", short_help="Uninstall shell completion files/code"
)
@click.argument("shell", type=click.Choice([t.value for t in ShellType]))
@click.option(
    "--path",
    type=click.Path(file_okay=True, dir_okay=False, readable=True),
    help="Custom installation path of the code to be evaluated by the shell. "
    "The standard installation path is used by default.",
)
def system_completion_uninstall(shell, path):
    shell = ShellType(shell)
    path = path or get_completion_install_path(shell)
    uninstall_completion_code(shell, path)
    click.echo(
        "ZhiXin CLI completion has been uninstalled for %s shell from %s \n"
        "Please restart a current shell session."
        % (click.style(shell.name, fg="cyan"), click.style(path, fg="blue"))
    )
