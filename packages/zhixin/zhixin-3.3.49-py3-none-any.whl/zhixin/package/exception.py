from zhixin import util
from zhixin.exception import UserSideException


class PackageException(UserSideException):
    pass


class ManifestException(PackageException):
    pass


class UnknownManifestError(ManifestException):
    pass


class ManifestParserError(ManifestException):
    pass


class ManifestValidationError(ManifestException):
    def __init__(self, messages, data, valid_data):
        super().__init__()
        self.messages = messages
        self.data = data
        self.valid_data = valid_data

    def __str__(self):
        return (
            "Invalid manifest fields: %s. \nPlease check specification -> "
            "https://docs.ZhiXin-Semi.com/page/librarymanager/config.html"
            % self.messages
        )


class MissingPackageManifestError(ManifestException):
    MESSAGE = "Could not find one of '{0}' manifest files in the package"


class UnknownPackageError(PackageException):
    MESSAGE = (
        "Could not find the package with '{0}' requirements for your system '%s'"
        % util.get_systype()
    )


class NotGlobalLibDir(PackageException):
    MESSAGE = (
        "The `{0}` is not a ZhiXin project.\n\n"
        "To manage libraries in global storage `{1}`,\n"
        "please use `zhixin lib --global {2}` or specify custom storage "
        "`zhixin lib --storage-dir /path/to/storage/ {2}`.\n"
        "Check `zhixin lib --help` for details."
    )
