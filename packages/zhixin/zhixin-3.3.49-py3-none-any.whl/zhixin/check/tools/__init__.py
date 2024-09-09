from zhixin import exception
from zhixin.check.tools.clangtidy import ClangtidyCheckTool
from zhixin.check.tools.cppcheck import CppcheckCheckTool
from zhixin.check.tools.pvsstudio import PvsStudioCheckTool


class CheckToolFactory:
    @staticmethod
    def new(tool, project_dir, config, envname, options):
        cls = None
        if tool == "cppcheck":
            cls = CppcheckCheckTool
        elif tool == "clangtidy":
            cls = ClangtidyCheckTool
        elif tool == "pvs-studio":
            cls = PvsStudioCheckTool
        else:
            raise exception.ZhixinException("Unknown check tool `%s`" % tool)
        return cls(project_dir, config, envname, options)
