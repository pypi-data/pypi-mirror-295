from zhixin.debug.config.base import DebugConfigBase


class RenodeDebugConfig(DebugConfigBase):
    DEFAULT_PORT = ":3333"
    GDB_INIT_SCRIPT = """
define zx_reset_halt_target
    monitor machine Reset
    $LOAD_CMDS
    monitor start
end

define zx_reset_run_target
    zx_reset_halt_target
end

target extended-remote $DEBUG_PORT
$LOAD_CMDS
$INIT_BREAK
monitor start
"""

    @property
    def server_ready_pattern(self):
        return super().server_ready_pattern or (
            "GDB server with all CPUs started on port"
        )
