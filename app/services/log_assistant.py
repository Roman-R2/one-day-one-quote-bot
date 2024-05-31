import sys
import traceback
from enum import Enum


class LogLevel(Enum):
    debug = 'debug'
    error = 'error'
    critical = 'critical'


class LogAssistant:
    def __init__(self, logger, log_level, message: str = '', with_trace: bool = False, with_print: bool = False):
        self.logger = logger
        self.log_level = log_level
        self.message = message
        self.with_trace = with_trace
        self.with_print = with_print
        self.error_type, self.error_value, self.error_trace = sys.exc_info()

    def __get_custom_traceback(self) -> str:
        custom_traceback = "\n"
        for line in [
            (item.filename, item.lineno, item.name, item._line)
            for item in traceback.extract_tb(self.error_trace)
        ]:
            custom_traceback = f"{custom_traceback}File {line[0]}, line {line[1]} in {line[2]}\n\t{line[3]}\n"

        return custom_traceback

    def __get_message_with_trace(self):
        return (
            f"{self.message}\n"
            f"Type: {self.error_type}\n"
            f"Value: {self.error_value}\n"
            f"Traceback: {self.__get_custom_traceback()}")

    def _get_message(self):
        if self.with_trace:
            return self.__get_message_with_trace()
        return self.message

    def _write(self):
        this_message = self._get_message()
        if self.with_print:
            print(this_message)
        if self.log_level == LogLevel.debug.value:
            self.logger.debug(this_message)
        if self.log_level == LogLevel.error.value:
            self.logger.error(this_message)
        if self.log_level == LogLevel.critical.value:
            self.logger.critical(this_message)

    @classmethod
    def put_to_log(cls, logger, message: str = '', log_level=LogLevel.debug, with_trace: bool = False,
                   with_print: bool = False):
        return cls(logger=logger, log_level=log_level, message=message, with_trace=with_trace,
                   with_print=with_print)._write()
