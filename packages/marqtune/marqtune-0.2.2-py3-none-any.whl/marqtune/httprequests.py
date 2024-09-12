import copy
import json
from typing import get_args, Any, Callable, Dict, Literal, List, Optional, Tuple, Union
import requests
from requests import JSONDecodeError

from marqtune.config import Config

HTTP_OPERATIONS = Literal["delete", "get", "post", "put"]
ALLOWED_OPERATIONS: Tuple[HTTP_OPERATIONS, ...] = get_args(HTTP_OPERATIONS)
session = requests.Session()

OPERATION_MAPPING = {
    'delete': session.delete,
    'get': session.get,
    'post': session.post,
    'put': session.put
}


class HttpRequests:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.headers = {'x-api-key': config.api_key} if config.api_key else {}

    def _operation(self, method: HTTP_OPERATIONS) -> Callable:
        if method not in ALLOWED_OPERATIONS:
            raise ValueError("{} not an allowed operation {}".format(method, ALLOWED_OPERATIONS))

        return OPERATION_MAPPING[method]

    def _construct_path(self, path: str) -> str:
        """Augment the URL request path based if telemetry is required."""
        if path.endswith("/"):
            path = path[:-1]
        url = f"{self.config.url}/{path}"
        return url

    def send_request(
        self,
        http_operation: HTTP_OPERATIONS,
        path: str,
        body: Optional[Union[Dict[str, Any], List[Dict[str, Any]], List[str], str]] = None,
        content_type: Optional[str] = None,
    ) -> Any:
        req_headers = copy.deepcopy(self.headers)

        if content_type is not None and content_type:
            req_headers['Content-Type'] = content_type

        if not isinstance(body, (bytes, str)) and body is not None:
            body = json.dumps(body)

        response = self._operation(http_operation)(
            url=self._construct_path(path),
            headers=req_headers,
            data=body,
            verify=True
        )
        return self._validate(response)

    def get(
        self, path: str,
        body: Optional[Union[Dict[str, Any], List[Dict[str, Any]], List[str], str]] = None,
    ) -> Any:
        content_type = None
        if body is not None:
            content_type = 'application/json'
        return self.send_request('get', path=path, body=body, content_type=content_type)

    def post(
        self,
        path: str,
        body: Optional[Union[Dict[str, Any], List[Dict[str, Any]], List[str], str]] = None,
        content_type: Optional[str] = 'application/json'
    ) -> Any:
        return self.send_request('post', path, body, content_type)

    def put(
        self,
        path: str,
        body: Optional[Union[Dict[str, Any], List[Dict[str, Any]], List[str], str]] = None,
        content_type: Optional[str] = None
    ) -> Any:
        if body is not None:
            content_type = 'application/json'
        return self.send_request('put', path, body, content_type)

    def delete(
        self,
        path: str,
        body: Optional[Union[Dict[str, Any], List[Dict[str, Any]], List[str]]] = None
    ) -> Any:
        return self.send_request('delete', path, body)

    @staticmethod
    def __to_json(
        response: requests.Response
    ) -> Any:
        if response.content == b'':
            return response
        return response.json()

    @staticmethod
    def _validate(
        response: requests.Response
    ) -> Any:
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # try to append the message from the response into the HTTPError to be more user-friendly:
            try:
                e.args = (e.args[0], response.json()['message'])
            except (JSONDecodeError, KeyError):
                # we failed to modify the message as the response was in an unexpected format,
                # we're going to re-raise the original error below anyway, so just pass:
                pass
            raise
        return HttpRequests.__to_json(response)
