from zhixin.debug.config.base import DebugConfigBase
from zhixin.debug.exception import DebugInvalidOptionsError
from zhixin.device.finder import SerialPortFinder, is_pattern_port


class BlackmagicDebugConfig(DebugConfigBase):
    GDB_INIT_SCRIPT = """
define zx_reset_halt_target
    set language c
    set *0xE000ED0C = 0x05FA0004
    set $busy = (*0xE000ED0C & 0x4)
    while ($busy)
        set $busy = (*0xE000ED0C & 0x4)
    end
    set language auto
end

define zx_reset_run_target
    zx_reset_halt_target
end

target extended-remote $DEBUG_PORT
monitor swdp_scan
attach 1
set mem inaccessible-by-default off
$LOAD_CMDS
$INIT_BREAK

set language c
set *0xE000ED0C = 0x05FA0004
set $busy = (*0xE000ED0C & 0x4)
while ($busy)
    set $busy = (*0xE000ED0C & 0x4)
end
set language auto
"""

    @property
    def port(self):
        # pylint: disable=assignment-from-no-return
        initial_port = DebugConfigBase.port.fget(self)
        if initial_port and not is_pattern_port(initial_port):
            return initial_port
        port = SerialPortFinder(
            board_config=self.board_config,
            upload_protocol=self.tool_name,
            prefer_gdb_port=True,
        ).find(initial_port)
        if port:
            return port
        raise DebugInvalidOptionsError(
            "Please specify `debug_port` for the working environment"
        )

    @port.setter
    def port(self, value):
        self._port = value
