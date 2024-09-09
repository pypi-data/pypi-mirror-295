from zhixin.debug.config.base import DebugConfigBase


class GenericDebugConfig(DebugConfigBase):
    DEFAULT_PORT = ":3333"
    GDB_INIT_SCRIPT = """
define zx_reset_halt_target
    monitor reset halt
end

define zx_reset_run_target
    monitor reset
end

target extended-remote $DEBUG_PORT
monitor init
$LOAD_CMDS
zx_reset_halt_target
$INIT_BREAK
"""
