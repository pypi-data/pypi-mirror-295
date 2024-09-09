from zhixin.device.monitor.filters.base import DeviceMonitorFilterBase


class SendOnEnter(DeviceMonitorFilterBase):
    NAME = "send_on_enter"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._buffer = ""

        if self.options.get("eol") == "CR":
            self._eol = "\r"
        elif self.options.get("eol") == "LF":
            self._eol = "\n"
        else:
            self._eol = "\r\n"

    def tx(self, text):
        self._buffer += text
        if self._buffer.endswith(self._eol):
            text = self._buffer
            self._buffer = ""
            return text
        return ""
