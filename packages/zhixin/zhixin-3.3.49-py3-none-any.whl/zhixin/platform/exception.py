from zhixin.exception import UserSideException


class PlatformException(UserSideException):
    pass


class UnknownPlatform(PlatformException):
    MESSAGE = "Unknown development platform '{0}'"


class IncompatiblePlatform(PlatformException):
    MESSAGE = (
        "Development platform '{0}' is not compatible with ZhiXin Core v{1} and "
        "depends on ZhiXin Core {2}.\n"
    )


class UnknownBoard(PlatformException):
    MESSAGE = "Unknown board ID '{0}'"


class InvalidBoardManifest(PlatformException):
    MESSAGE = "Invalid board JSON manifest '{0}'"


class UnknownFramework(PlatformException):
    MESSAGE = "Unknown framework '{0}'"


class BuildScriptNotFound(PlatformException):
    MESSAGE = "Invalid path '{0}' to build script"
