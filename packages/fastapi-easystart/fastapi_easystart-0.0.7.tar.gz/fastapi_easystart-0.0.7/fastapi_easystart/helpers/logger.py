import logging
import os
from enum import Enum

from uvicorn.logging import DefaultFormatter


class LogTypeEnum(str, Enum):
    """
    Enumeration for log types to standardize log level names.
    """
    INFO = "info"
    ERROR = "error"
    WARNING = "warning"
    DEBUG = "debug"
    CRITICAL = "critical"


class LoggerConfigurator:
    """
    LoggerConfigurator is a class that encapsulates the configuration of loggers.
    It includes a custom log formatter and methods to initialize loggers and log messages.
    """

    # Log format string
    FORMAT = "%(levelprefix)s %(asctime)s [%(threadName)s] [%(name)s] (%(request_id)s) %(message)s"

    class CustomLogFormatter(DefaultFormatter):
        """
        CustomLogFormatter extends the default formatter to include a custom field 'request_id'.
        """

        def format(self, record: logging.LogRecord) -> str:
            # Add a 'request_id' to the log record if it does not exist
            record.request_id = record.__dict__.get("request_id", "")
            return super().format(record)

    @classmethod
    def init_logger(cls, logger_name: str = "default-logger") -> logging.Logger:
        """
        Initializes a logger with the specified name and configures it with a custom formatter.

        :param logger_name: The name of the logger to initialize
        :return: Configured logger instance
        """
        # Create or get the logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Create a custom formatter instance
        formatter_custom = cls.CustomLogFormatter(cls.FORMAT, datefmt="%Y-%m-%d %H:%M:%S")

        # Add the formatter to the console handler
        console_handler.setFormatter(formatter_custom)

        # Add the console handler to the logger
        logger.addHandler(console_handler)

        return logger

    @classmethod
    def log_message(cls, logger_name: str, message: str, allow_logging: bool = True,
                    ignore_dev: bool = False, log_type: LogTypeEnum = LogTypeEnum.INFO) -> None:
        """
        Logs a message using a logger with the specified name based on the application settings,
        ignore_dev flag, and log_type.

        :param logger_name: The name of the logger to use.
        :param message: The message to be logged.
        :param allow_logging: If True, the message will be logged.
        :param ignore_dev: If True, the message is always printed. If False, the message is only printed in debug mode.
        :param log_type: The type of log (info, error, warning, debug).
        """
        # Get the logger with the specified name
        logger = logging.getLogger(logger_name)

        # environment
        environment = os.getenv("FA_ENVIRONMENT")

        if ignore_dev or True if environment in ["dev", "local"] else False:
            print(message)

        if allow_logging:
            # Use the appropriate logging method based on log_type
            getattr(logger, log_type.value.lower(), logger.info)(message)


# Usage example
log = LoggerConfigurator.init_logger(logger_name="main-logger")
# log.info("Logger initialized and ready to use")

# Logging message using the class method
# LoggerConfigurator.log_message("main-logger", "This is a log message", log_type=LogTypeEnum.INFO)
