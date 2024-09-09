import click

from zhixin.device.list.command import device_list_cmd
from zhixin.device.monitor.command import device_monitor_cmd


@click.group(
    "device",
    commands=[
        device_list_cmd,
        device_monitor_cmd,
    ],
    short_help="Device manager & Serial/Socket monitor",
)
def cli():
    pass
