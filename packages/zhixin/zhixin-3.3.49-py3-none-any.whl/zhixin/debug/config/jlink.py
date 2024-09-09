from zhixin.debug.config.base import DebugConfigBase


class JlinkDebugConfig(DebugConfigBase):
    DEFAULT_PORT = ":2331"
    GDB_INIT_SCRIPT = """
define zx_reset_halt_target
    monitor reset
    monitor halt
end

define zx_reset_run_target
    monitor clrbp
    monitor reset
    monitor go
end

target extended-remote $DEBUG_PORT
monitor clrbp
monitor speed auto
zx_reset_halt_target
$LOAD_CMDS
$INIT_BREAK
"""

    @property
    def server_ready_pattern(self):
        return super().server_ready_pattern or ("Waiting for GDB connection")
