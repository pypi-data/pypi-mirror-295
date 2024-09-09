from zhixin.exception import ZhixinException, UserSideException


class UnitTestError(ZhixinException):
    pass


class TestDirNotExistsError(UnitTestError, UserSideException):
    MESSAGE = (
        "A test folder '{0}' does not exist.\nPlease create 'test' "
        "directory in the project root and put a test suite.\n"
    )


class UnitTestSuiteError(UnitTestError):
    pass
