from zhixin.debug.config.base import DebugConfigBase


class QemuDebugConfig(DebugConfigBase):
    DEFAULT_PORT = ":1234"
    GDB_INIT_SCRIPT = """
define zx_reset_halt_target
    monitor system_reset
end

define zx_reset_run_target
    monitor system_reset
end

target extended-remote $DEBUG_PORT
$LOAD_CMDS
zx_reset_halt_target
$INIT_BREAK
"""
