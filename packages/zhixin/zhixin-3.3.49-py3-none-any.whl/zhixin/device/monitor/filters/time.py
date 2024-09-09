from datetime import datetime

from zhixin.device.monitor.filters.base import DeviceMonitorFilterBase


class Timestamp(DeviceMonitorFilterBase):
    NAME = "time"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._line_started = False

    def rx(self, text):
        if self._line_started and "\n" not in text:
            return text
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        if not self._line_started:
            self._line_started = True
            text = "%s > %s" % (timestamp, text)
        if text.endswith("\n"):
            self._line_started = False
            return text[:-1].replace("\n", "\n%s > " % timestamp) + "\n"
        return text.replace("\n", "\n%s > " % timestamp)
