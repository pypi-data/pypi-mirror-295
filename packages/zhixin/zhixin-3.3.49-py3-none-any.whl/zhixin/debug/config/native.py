from zhixin.compat import IS_WINDOWS
from zhixin.debug.config.base import DebugConfigBase


class NativeDebugConfig(DebugConfigBase):
    GDB_INIT_SCRIPT = """
define zx_reset_halt_target
end

define zx_reset_run_target
end

define zx_restart_target
end

$INIT_BREAK
""" + (
        "set startup-with-shell off" if not IS_WINDOWS else ""
    )
