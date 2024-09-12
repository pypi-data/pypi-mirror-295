from typing import Callable

from django import http


class EarlyReturn(Exception):
    """
    Exception which views may raise, when using EarlyReturnMiddleware, to short-circuit view processing
    """

    def __init__(self, response: http.HttpResponse):
        self.response = response


class EarlyReturnMiddleware:
    """
    Middleware which lets views/view decorators raise EarlyReturn to short-circuit processing
    """

    def __init__(self, get_response: Callable[[http.HttpRequest], http.HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: http.HttpRequest):
        return self.get_response(request)

    def process_exception(self, request: http.HttpRequest, exception: Exception):
        if isinstance(exception, EarlyReturn):
            return exception.response
