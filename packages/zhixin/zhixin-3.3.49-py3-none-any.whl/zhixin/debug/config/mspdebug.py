from zhixin.debug.config.base import DebugConfigBase


class MspdebugDebugConfig(DebugConfigBase):
    DEFAULT_PORT = ":2000"
    GDB_INIT_SCRIPT = """
define zx_reset_halt_target
end

define zx_reset_run_target
end

target remote $DEBUG_PORT
monitor erase
$LOAD_CMDS
zx_reset_halt_target
$INIT_BREAK
"""
