import serial

from zhixin.device.monitor.filters.base import DeviceMonitorFilterBase


class Hexlify(DeviceMonitorFilterBase):
    NAME = "hexlify"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._counter = 0

    def set_running_terminal(self, terminal):
        # force to Latin-1, issue #4732
        if terminal.input_encoding == "UTF-8":
            terminal.set_rx_encoding("Latin-1")
        super().set_running_terminal(terminal)

    def rx(self, text):
        result = ""
        for c in serial.iterbytes(text):
            if (self._counter % 16) == 0:
                result += "\n{:04X} | ".format(self._counter)
            asciicode = ord(c)
            if asciicode <= 255:
                result += "{:02X} ".format(asciicode)
            else:
                result += "?? "
            self._counter += 1
        return result
