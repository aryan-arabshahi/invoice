from enum import Enum
from typing import Union
from flask import make_response
from flask import Response


class ResponseStatus(Enum):
    SUCCESS = 'success'
    FAILED = 'failed'


class HttpResponse:

    def success(self, data: Union[dict, list, str] = None, message: str = None, http_status: int = 200) -> Response:
        """Create a success response

        Keyword Arguments:
            data {Union[dict, list]} -- (default: {None})
            message {str} -- (default: {None})
            http_status {int} -- (default: {200})
        
        Returns:
            Response
        """
        return make_response({
            'status': ResponseStatus.SUCCESS.value,
            'message': message or 'request_succeeded',
            'data': data if data is not None else {},
        }, http_status)

    def failed(self, http_status: int, message: str = None, data: dict = None) -> Response:
        """Create a failed response

        Arguments:
            http_status {int}

        Keyword Arguments:
            message {str} -- (default: {None})
            data {dict} -- (default: {None})

        Returns:
            Response
        """
        return make_response({
            'status': ResponseStatus.FAILED.value,
            'message': message or 'request_failed',
            'data': data if data is not None else {},
        }, http_status)
