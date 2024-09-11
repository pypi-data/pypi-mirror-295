import logging
from ceonstock.log import formats


class ColoredFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    green = "\x1b[32m"
    blue = "\x1b[34m"
    cyan = "\x1b[36m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    _reset = "\x1b[0m"
    msg_format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    def __init__(self, string_for_format: str):
        self.msg_format = ColoredFormatter.msg_format
        if string_for_format:
            self.msg_format = string_for_format

    def get_format(self, levelno):
        COLORS = {
            logging.DEBUG: ColoredFormatter.blue,
            logging.INFO: ColoredFormatter.grey,
            logging.WARNING: ColoredFormatter.yellow,
            logging.ERROR: ColoredFormatter.red,
            logging.CRITICAL: ColoredFormatter.bold_red,
        }
        chosen_color = COLORS.get(levelno, "")
        return chosen_color + self.msg_format + ColoredFormatter._reset

    def format(self, record):
        log_fmt = self.get_format(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


DEV = ColoredFormatter(formats.DEV)
PROD = logging.Formatter(formats.PROD)
