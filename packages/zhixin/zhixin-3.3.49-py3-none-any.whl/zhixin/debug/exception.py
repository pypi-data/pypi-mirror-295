from zhixin.exception import ZhixinException, UserSideException


class DebugError(ZhixinException):
    pass


class DebugSupportError(DebugError, UserSideException):
    MESSAGE = (
        "Currently, ZhiXin does not support debugging for `{0}`.\n"
        "Please request support at https://github.com/zhixin/"
        "zhixin-core/issues \nor visit -> https://docs.ZhiXin-Semi.com"
        "/page/plus/debugging.html"
    )


class DebugInvalidOptionsError(DebugError, UserSideException):
    pass


class DebugInitError(DebugError, UserSideException):
    pass
