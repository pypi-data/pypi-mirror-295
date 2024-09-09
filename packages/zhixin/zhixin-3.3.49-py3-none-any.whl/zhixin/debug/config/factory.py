import importlib
import re

from zhixin.debug.config.generic import GenericDebugConfig
from zhixin.debug.config.native import NativeDebugConfig


class DebugConfigFactory:
    @staticmethod
    def get_clsname(name):
        name = re.sub(r"[^\da-z\_\-]+", "", name, flags=re.I)
        return "%sDebugConfig" % name.lower().capitalize()

    @classmethod
    def new(cls, platform, project_config, env_name):
        board_id = project_config.get("env:" + env_name, "board")
        config_cls = None
        tool_name = None
        if board_id:
            tool_name = platform.board_config(
                project_config.get("env:" + env_name, "board")
            ).get_debug_tool_name(project_config.get("env:" + env_name, "debug_tool"))
        try:
            mod = importlib.import_module("zhixin.debug.config.%s" % tool_name)
            config_cls = getattr(mod, cls.get_clsname(tool_name))
        except ModuleNotFoundError:
            config_cls = (
                GenericDebugConfig if platform.is_embedded() else NativeDebugConfig
            )
        return config_cls(platform, project_config, env_name)
