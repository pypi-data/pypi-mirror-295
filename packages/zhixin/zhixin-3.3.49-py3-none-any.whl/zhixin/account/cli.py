import click

from zhixin.account.commands.destroy import account_destroy_cmd
from zhixin.account.commands.forgot import account_forgot_cmd
from zhixin.account.commands.login import account_login_cmd
from zhixin.account.commands.logout import account_logout_cmd
from zhixin.account.commands.password import account_password_cmd
from zhixin.account.commands.register import account_register_cmd
from zhixin.account.commands.show import account_show_cmd
from zhixin.account.commands.token import account_token_cmd
from zhixin.account.commands.update import account_update_cmd


@click.group(
    "account",
    commands=[
        account_destroy_cmd,
        account_forgot_cmd,
        account_login_cmd,
        account_logout_cmd,
        account_password_cmd,
        account_register_cmd,
        account_show_cmd,
        account_token_cmd,
        account_update_cmd,
    ],
    short_help="Manage ZhiXin account",
)
def cli():
    pass
