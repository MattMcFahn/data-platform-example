"""
 Module to configure logging handlers, filters and levels in the application entrypoint.
 Logs are passed via the stdout handler to the lambda's logs as json, and read into CloudWatch.
"""
from logging import WARNING, Filter, Formatter, Handler, StreamHandler, getLevelName, getLogger, root
from sys import stdout
from typing import List

from pythonjsonlogger.jsonlogger import JsonFormatter

APPLICATION_LOG_LEVEL = getLevelName("INFO")


class AppFilter(Filter):  # pylint: disable=too-few-public-methods
    """
    Class that can act on a log handler to filter all records passed to the handle
    and add fields that should be present in all logs
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def filter(self, record) -> bool:
        """Impose relevant fields on records"""
        record.component = "etl-lambda"

        return True


def get_log_handlers() -> List[Handler]:
    """Define and format logging handlers to use in the application, imposing on the logging module"""
    # pylint: disable=redefined-builtin, implicit-str-concat
    stream_handler = StreamHandler()

    # Used for local v deployed logging: https://docs.python.org/3/library/io.html#io.IOBase.isatty
    if stdout.isatty():
        terminal_format = """[%(asctime)s.%(msecs)03d] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"""

        stream_handler.setFormatter(fmt=Formatter(terminal_format))
    else:
        # NOTE: Milliseconds implementation doesn't work via JSONFormatter as it doesn't expose the right methods on the
        # parent class
        json_format = """
        [%(asctime)s.%(msecs)03d] %(levelname)s <%(correlationId)s> " "[%(name)s.%(funcName)s:%(lineno)d] %(message)s
        """
        date_format = "%Y-%m-%dT%H:%M:%S"

        rename_fields = {"asctime": "@timestamp", "levelname": "level"}
        simple_json_formatter = JsonFormatter(fmt=json_format, datefmt=date_format, rename_fields=rename_fields)
        stream_handler.setFormatter(simple_json_formatter)

    app_filter = AppFilter()
    stream_handler.addFilter(app_filter)

    return [handler for handler in [stream_handler] if handler]


def setup_logging():
    """Configures logging with a chosen formatter."""
    handlers = get_log_handlers()

    # Pass handlers and level back to the root logger
    root.handlers = handlers
    root.setLevel(APPLICATION_LOG_LEVEL)

    # pylint: disable=no-member
    for name in root.manager.loggerDict.keys():
        logger = getLogger(name)
        logger.handlers = []
        logger.propagate = True

    # Overrides for module specific loggers
    modules = {
        "botocore": WARNING,
        "boto3": WARNING,
        "s3transfer": WARNING,
        "urllib3": WARNING,
    }
    for name, level in modules.items():
        logger = getLogger(name)
        logger.handlers = []
        logger.setLevel(level)
        logger.propagate = True
