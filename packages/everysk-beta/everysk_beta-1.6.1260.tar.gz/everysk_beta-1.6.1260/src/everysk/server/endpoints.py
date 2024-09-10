###############################################################################
#
# (C) Copyright 2024 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
__all__ = ['BaseEndpoint', 'JSONEndpoint']
from typing import Any, Generator
from starlette.types import Receive, Scope, Send

from everysk.config import settings
from everysk.core.exceptions import HttpError
from everysk.core.log import Logger, LoggerManager, _get_trace_data
from everysk.core.serialize import loads
from everysk.server.requests import Request, JSONRequest
from everysk.server.responses import Response, JSONResponse


log = Logger(__name__)
HTTP_METHODS = ('GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS')
HTTP_STATUS_CODES_LOG = settings.EVERYSK_SERVER_CODES_LOG


class BaseEndpoint:
    # Based in starlette.endpoints.HTTPEndpoint
    ## Private attributes
    _allowed_methods: list[str] = None
    _request_class: Request = Request

    ## Public attributes
    receive: Receive = None
    request: Request = None
    scope: Scope = None
    send: Send = None

    ## Private methods
    def __init__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        Base class for all endpoints in the application.

        Args:
            scope (Scope): ASGI scope dictionary.
            receive (Receive): ASGI receive data.
            send (Send): ASGI send data.

        Raises:
            HttpError: 500 - Request is not an HTTP request.
        """
        type_request = scope.get('type', '')
        if type_request.lower() != 'http':
            raise HttpError(status_code=500, msg='Request is not an HTTP request.')

        self._allowed_methods = [method for method in HTTP_METHODS if hasattr(self, method.lower())]
        self.receive = receive
        self.request = self._request_class(scope, receive=receive)
        self.scope = scope
        self.send = send

    def __await__(self) -> Generator[Any, None, None]:
        """
        Method to allow the use of the await keyword in the class.
        This method will call the dispatch method and return the result.
        It's the default behavior of the Starlette HTTPEndpoint class.
        Don't change this method.
        """
        return self.dispatch().__await__()

    ## Public sync methods
    def get_http_headers(self) -> dict[str, str]:
        """
        Get the HTTP headers from the request.
        Returns dictionary were the key is the header name in lower case and the value is the header value.
        """
        return dict(self.request.headers)

    def get_http_method_function(self) -> callable:
        """
        Get the function that for the http method of the request.
        If the function doesn't exist, it will return the method_not_allowed function.
        """
        name = self.get_http_method_name()
        return getattr(self, name, self.method_not_allowed)

    def get_http_method_name(self) -> str:
        """
        Get the name of the HTTP method from the request.
        If the request method is HEAD and the class doesn't
        have a head method, it will return get instead.
        """
        if self.request.method == 'HEAD' and not hasattr(self, 'head'):
            name = 'get'
        else:
            name = self.request.method.lower()

        return name

    ## Public async methods
    async def dispatch(self) -> None:
        """
        Main method that will always be executed for each request, takes
        the function related to the HTTP method of the request and executes it.
        """
        # Because the ASGI protocol copy the context to the event loop
        # for every request, we create an empty LoggerManager to avoid
        # shared values between requests.
        with LoggerManager(http_headers={}, http_payload={}, labels={}, stacklevel=None, traceback=''):
            headers = self.get_http_headers()
            # Insert the headers in the Logger Context to propagate them to the logs
            with LoggerManager(http_headers=headers):
                try:
                    response = await self.get_http_response()
                except Exception as error: # pylint: disable=broad-except
                    # If something goes wrong, we catch the exception and return a response
                    response = await self.get_http_exception_response(error)

                    # We only log internal server errors in GCP
                    if getattr(error, 'status_code', 500) in HTTP_STATUS_CODES_LOG:
                        payload = await self.get_http_payload()
                        # Headers are already in the LoggerManager
                        log.error(str(error), extra={'http_payload': payload})

                await response(self.scope, self.receive, self.send)

        # To avoid shared values between requests, we reset the LoggerManager
        LoggerManager.reset()

    async def get_http_exception_response(self, error: Exception) -> Response:
        """
        Method to return a response when an exception is raised during the request.

        Args:
            error (Exception): The exception raised during the request.
        """
        status_code = getattr(error, 'status_code', 500)
        return Response(str(error), status_code=status_code)

    async def get_http_payload(self) -> bytes:
        """
        Get the HTTP payload from the request.
        The payload is the body of the request and it's a bytes object.
        """
        return await self.request.body()

    async def get_http_response(self) -> Response:
        """
        Get the correct function for the HTTP method of the request
        and execute it to create a response.
        If the method doesn't exist, it will return a 405 response.
        """
        method_function = self.get_http_method_function()
        return await method_function()

    async def method_not_allowed(self) -> None:
        """
        Default method for when the HTTP method is not found in the class.

        Raises:
            HttpError: 405 - Method not allowed
        """
        raise HttpError(status_code=405, msg=f'Method {self.request.method} not allowed.')


class JSONEndpoint(BaseEndpoint):
    ## Private attributes
    _request_class: JSONRequest = JSONRequest

    ## Public attributes
    rest_key_name: str = Undefined
    rest_key_value: str = Undefined

    def __init__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        Class to handle JSON requests and responses.
        Inherit from this class and implement the HTTP methods to create an endpoint.

        Args:
            scope (Scope): ASGI scope dictionary.
            receive (Receive): ASGI receive data.
            send (Send): ASGI send data.
        """
        super().__init__(scope, receive, send)

        if self.rest_key_name is Undefined:
            self.rest_key_name = settings.EVERYSK_SERVER_REST_KEY_NAME

        if self.rest_key_value is Undefined:
            self.rest_key_value = settings.EVERYSK_SERVER_REST_KEY_VALUE

    def check_rest_key(self) -> bool:
        """
        Check if the rest key is present in the request headers and if it's the correct value.
        If the rest key name or value is not set, it will always return True.
        """
        if not self.rest_key_name or not self.rest_key_value:
            return True

        rest_key_value = self.request.headers.get(self.rest_key_name)
        return rest_key_value == self.rest_key_value

    async def get_http_exception_response(self, error: Exception) -> JSONResponse:
        """
        Method to return a JSONResponse when an exception is raised during the request.
        The trace_id is added to the response to help with debugging.

        Args:
            error (Exception): The exception raised during the request.

        Returns:
            JSONResponse: A JSONResponse with the error message, status code and trace_id.
        """
        trace_data = _get_trace_data(headers=self.get_http_headers())
        msg = str(error)
        status_code = getattr(error, 'status_code', 500)
        return JSONResponse({'error': msg, 'code': status_code, 'trace_id': trace_data['trace_id']}, status_code=status_code)

    async def get_http_payload(self) -> Any:
        """
        Get the HTTP payload from the request and deserialize it to a
        Python object or an empty dict if the request.body is empty.
        """
        body = await super().get_http_payload()
        if body:
            return loads(body, protocol='json', use_undefined=True)

        return {}

    async def get_http_response(self) -> JSONResponse:
        """
        Changes the return of the get_http_response method to return a JSONResponse.
        If the response is not a Response object, it will be converted to a JSONResponse
        otherwise it will be returned as is.
        If the rest key is incorrect, it will raise a 401 error.

        Raises:
            HttpError: 401 - Unauthorized access to this resource.
        """
        if not self.check_rest_key():
            raise HttpError(status_code=401, msg='Unauthorized access to this resource.')

        response = await super().get_http_response()
        if not isinstance(response, Response):
            response = JSONResponse(response)

        return response
