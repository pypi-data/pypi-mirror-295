import logging
from ceonstock.log import formatters, handlers, module_logger

self_logger = module_logger()


def setup_root_logger(level="DEBUG"):
    """Apply a custom formatter to the root logger"""
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    if not root_logger.handlers:
        # If there is no handler on the root logger, add the default stream handler
        root_logger.addHandler(handlers.stream_handler())
        return
    # If there are already handlers on the root logger, update their formatter
    self_logger.warning(
        f"Got existing root_logger handlers. Replacing formatters for handlers: {root_logger.handlers}"
    )
    new_formatter = formatters.DEV
    for handler in root_logger.handlers:
        self_logger.info(f"Updated handler {handler} to use formatter: {new_formatter}")
        handler.setFormatter(new_formatter)


def all_loggers() -> list[logging.Logger]:
    loggers = [logging.getLogger()]  # get the root logger
    loggers = loggers + [
        logging.getLogger(name) for name in logging.root.manager.loggerDict
    ]
    return loggers


def set_all_ceonstock_loggers_level(level: str):
    self_logger.info(f"Setting ceonstock loggers level to: {level}")
    for logger in all_loggers():
        if logger.name.startswith("ceonstock"):
            self_logger.debug(f"\t{logger.name}")
            logger.setLevel(level)


def set_stream_formatters(formatter: logging.Formatter):
    """Find all stream handlers and replace the formatter with the provided"""
