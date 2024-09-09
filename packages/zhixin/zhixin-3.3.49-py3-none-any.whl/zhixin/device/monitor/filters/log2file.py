import io
import os
from datetime import datetime

from zhixin.device.monitor.filters.base import DeviceMonitorFilterBase


class LogToFile(DeviceMonitorFilterBase):
    NAME = "log2file"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._log_fp = None

    def __call__(self):
        if not os.path.isdir("logs"):
            os.makedirs("logs")
        log_file_name = os.path.join(
            "logs", "device-monitor-%s.log" % datetime.now().strftime("%y%m%d-%H%M%S")
        )
        print("--- Logging an output to %s" % os.path.abspath(log_file_name))
        # pylint: disable=consider-using-with
        self._log_fp = io.open(log_file_name, "w", encoding="utf-8")
        return self

    def __del__(self):
        if self._log_fp:
            self._log_fp.close()

    def rx(self, text):
        self._log_fp.write(text)
        self._log_fp.flush()
        return text
