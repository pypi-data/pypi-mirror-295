import re

import click

from zhixin.account.validate import validate_orgname_teamname, validate_username


def validate_urn(value):
    value = str(value).strip()
    if not re.match(r"^prn:reg:pkg:(\d+):(\w+)$", value, flags=re.I):
        raise click.BadParameter("Invalid URN format.")
    return value


def validate_client(value):
    if ":" in value:
        validate_orgname_teamname(value)
    else:
        validate_username(value)
    return value
