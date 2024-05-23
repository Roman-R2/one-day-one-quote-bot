import sys
import traceback


class GetTraceback:
    """ Класс для ошибок вместе с traceback. """

    def __init__(self, message: str = '', verbose: bool = True):
        self.verbose = verbose
        self.error_type, self.error_value, self.error_trace = sys.exc_info()
        self.message = message
        self._message_with_trace = self.__construct_current_message(message=message)

    def _all(self):
        return self._message_with_trace

    def __construct_current_message(self, message: str):
        message = (
            f"{message}\n"
            f"Type: {self.error_type}\n"
            f"Value: {self.error_value}")
        if self.verbose:
            message = (
                f"{message}\n"
                f"Traceback: {self.__get_custom_traceback()}"
            )
        return message

    def __get_custom_traceback(self) -> str:
        custom_traceback = "\n"
        for line in [
            (item.filename, item.lineno, item.name, item._line)
            for item in traceback.extract_tb(self.error_trace)
        ]:
            custom_traceback = f"{custom_traceback}File {line[0]}, line {line[1]} in {line[2]}\n\t{line[3]}\n"

        return custom_traceback

    @classmethod
    def all(cls, message: str = '', verbose: bool = True):
        return cls(message=message, verbose=verbose)._all()
