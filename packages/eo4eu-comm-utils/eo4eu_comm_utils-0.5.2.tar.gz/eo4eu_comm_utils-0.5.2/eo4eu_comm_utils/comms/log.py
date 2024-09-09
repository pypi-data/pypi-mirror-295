import traceback
import logging
from .interface import Comm, LogLevel


class LogComm(Comm):
    def __init__(self, logger: logging.Logger, print_traceback: bool = False):
        self.logger = logger
        self.print_traceback = print_traceback

    def send(self, level: LogLevel, msg: str = "", *args, **kwargs):
        logging_level = level.to_logging_level()
        self.logger.log(
            logging_level,
            msg,
            exc_info = self.print_traceback and (logging_level >= logging.ERROR)
        )
