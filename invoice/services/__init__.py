from logging import getLogger
from traceback import format_exc
from invoice.logger import Logger


class BaseService:

    def __init__(self):
        # Setup the logger
        self.logger = Logger(
            getLogger(__name__),
            dict(prefix=getattr(self, 'LOG_PREFIX', getattr(self, 'LOG_PREFIX', self.__class__.__name__)))
        )

    def log_errors(self, message: str) -> None:
        """Add the traceback to the error logs

        Arguments:
            message {str}
        """
        self.logger.error(f'{message} - {format_exc()}')
