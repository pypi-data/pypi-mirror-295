"""
" ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ████████╗██████╗  ██████╗ ███╗   ██╗
" ██║  ██║██║   ██║████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗████╗  ██║
" ███████║██║   ██║██╔████╔██║███████║   ██║   ██████╔╝██║   ██║██╔██╗ ██║
" ██╔══██║██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║   ██║██║╚██╗██║
" ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║╚██████╔╝██║ ╚████║
" ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
"
"                   Copyright (C) 2023 Humatron, Inc.
"                          All rights reserved.
"""
import datetime
import json
import logging
import threading
import time
import uuid
from threading import Thread
from typing import NamedTuple, Optional, Callable

import requests


class RequestPayloadPart(NamedTuple):
    """
    Represents a part of a REST request payload.

    Attributes:
    -----------
    payload_id : str
        Unique identifier for the payload part.
    sender : str
        The sender of the payload.
    receiver : str
        The receiver of the payload.
    text : str
        The content of the payload.
    """

    payload_id: str
    sender: str
    receiver: str
    text: str

    @classmethod
    def make(cls, text: str, sender: str, receiver: str) -> 'RequestPayloadPart':
        """
        Creates a new RequestPayloadPart instance.

        Parameters:
        -----------
        text : str
            The content of the payload.
        sender : str
            The sender of the payload.
        receiver : str
            The receiver of the payload.

        Returns:
        --------
        RequestPayloadPart
            A new instance of RequestPayloadPart.
        """
        return cls(str(uuid.uuid4()), sender, receiver, text)


class RestRequest(NamedTuple):
    """
    Represents a REST request containing a list of payload parts.

    Attributes:
    -----------
    req_id : str
        Unique identifier for the request.
    payload : list[RequestPayloadPart]
        List of payload parts included in the request.
    req_tstamp : str
        Timestamp when the request was created.
    """

    req_id: str
    payload: list[RequestPayloadPart]
    req_tstamp: str

    @classmethod
    def make(cls, payload: list[RequestPayloadPart] | RequestPayloadPart) -> 'RestRequest':
        return cls(str(uuid.uuid4()), [payload] if not isinstance(payload, list) else payload, _utc_now_iso_format())


class RestHeartbeatRequest(NamedTuple):
    """
    Represents a heartbeat request to keep the connection alive.

    Attributes:
    -----------
    req_id : str
        Unique identifier for the request.
    req_tstamp : str
        Timestamp when the request was created.
    """

    req_id: str
    req_tstamp: str

    @classmethod
    def make(cls) -> 'RestHeartbeatRequest':
        """
        Creates a new RestHeartbeatRequest instance.

        Returns:
        --------
        RestHeartbeatRequest
            A new instance of RestHeartbeatRequest.
        """
        return cls(str(uuid.uuid4()), _utc_now_iso_format())


class ResponsePayloadPart(NamedTuple):
    """
    Represents a part of a REST response payload.

    Attributes:
    -----------
    payload_id : str
        Unique identifier for the response payload part.
    ref_payload_id : Optional[str]
        Reference to the request payload part ID, if applicable.
    sender : str
        The sender of the response payload.
    receiver : str
        The receiver of the response payload.
    text : str
        The content of the response payload.
    """

    ref_payload_id: Optional[str]
    sender: str
    receiver: str
    text: str


class RestResponse(NamedTuple):
    """
    Represents a REST response containing a list of response payload parts.

    Attributes:
    -----------
    resp_id : str
        Unique identifier for the response.
    payload : list[ResponsePayloadPart]
        List of payload parts included in the response.
    resp_tstamp : str
        Timestamp when the response was created.
    """

    resp_id: str
    payload: list[ResponsePayloadPart]
    resp_tstamp: str


def _utc_now_iso_format() -> str:
    """
    Returns the current UTC time in ISO format.

    Returns:
    --------
    str
        The current UTC time in ISO format, truncated to milliseconds.
    """
    return f'{datetime.datetime.utcnow().isoformat()[:-3]}Z'


def _post(
    url: str, headers: dict[str, str], req: RestRequest | RestHeartbeatRequest
) -> Optional[RestResponse]:
    """
    Sends a POST request to the server.

    Parameters:
    -----------
    url : str
        The server URL to send the request to.
    headers : dict[str, str]
        HTTP headers to include in the request.
    req : RestRequest | RestHeartbeatRequest
        The request to be sent, either a RestRequest or RestHeartbeatRequest.

    Returns:
    --------
    Optional[RestResponse]
        The response received from the server, or None if no response was received.

    Raises:
    -------
    ValueError
        If the response status code is not 200.
    """
    match req:
        case RestRequest(_):
            payload = [r._asdict() for r in req.payload]
            msg = {'req_cmd': 'request', 'req_id': req.req_id, 'req_tstamp': req.req_tstamp, 'payload': payload}
        case RestHeartbeatRequest(_):
            msg = {'req_cmd': 'heartbeat', 'req_id': req.req_id, 'req_tstamp': req.req_tstamp}
        case _:
            raise ValueError(f'Unexpected request type: {type(req)}')

    res = requests.post(url, json.dumps(msg), headers=headers)

    if res.status_code != 200:
        raise ValueError(f'Unexpected response code: {res.status_code}, content={res.json()}')

    resp_js = res.json()

    if not resp_js:
        return None

    payloads = [ResponsePayloadPart(
        ref_payload_id=p['ref_payload_id'] if 'ref_payload_id' in p else None,
        sender=p['sender'],
        receiver=p['receiver'],
        text=p['text']
    ) for p in resp_js['payload']]

    return RestResponse(resp_js['resp_id'], payloads, resp_js['resp_tstamp'])


def _mk_headers(token: str) -> dict[str, str]:
    """
    Creates HTTP headers required for the requests.

    Parameters:
    -----------
    token : str
        Authorization token to be included in the headers.

    Returns:
    --------
    dict[str, str]
        Dictionary of headers including Authorization and Content-Type.
    """
    return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}


class HumatronRestClient:
    """
    Synchronous REST client for sending requests and receiving responses.

    Attributes:
    -----------
    _server_url : str
        The server URL to send requests to.
    _headers : dict[str, str]
        HTTP headers to include in the requests.

    Methods:
    --------
    post(req: RestRequest | RestHeartbeatRequest) -> Optional[RestResponse]
        Sends a request to the server and returns the response.
    """

    def __init__(self, server_url: str, token: str):
        """
        Initializes the HumatronRestClient with the server URL and authorization token.

        Parameters:
        -----------
        server_url : str
            The server URL to send requests to.
        token : str
            Authorization token to be included in the headers.
        """
        self._server_url = server_url
        self._headers = _mk_headers(token)

    def post(self, req: RestRequest | RestHeartbeatRequest) -> Optional[RestResponse]:
        """
        Sends a request to the server and returns the response.

        Parameters:
        -----------
        req : RestRequest | RestHeartbeatRequest
            The request to be sent.

        Returns:
        --------
        Optional[RestResponse]
            The response received from the server, or None if no response was received.
        """
        return _post(self._server_url, self._headers, req)


_logger = logging.getLogger(__name__)

DFLT_HB_INTERVAL_SEC = 5


class HumatronAsyncRestClient:
    """
    Asynchronous REST client that sends requests and processes responses in the background.

    Attributes:
    -----------
    _server_url : str
        The server URL to send requests to.
    _headers : dict[str, str]
        HTTP headers to include in the requests.
    _on_resp_payload : Callable[[ResponsePayloadPart], None]
        Callback function to handle each response payload part.
    _on_hb_error : Optional[Callable[[Exception], None]]
        Optional callback function to handle errors during heartbeat.
    _hb_interval_sec : float
        Interval between heartbeat requests in seconds.

    Methods:
    --------
    start() -> None
        Starts the asynchronous client.
    close() -> None
        Stops the asynchronous client and waits for the thread to finish.
    post(req: RestRequest | RestHeartbeatRequest) -> None
        Sends a request to the server.
    """

    def __init__(
        self,
        server_url: str,
        token: str,
        on_resp_payload: Callable[[ResponsePayloadPart], None],
        on_hb_error: Optional[Callable[[Exception], None]] = None,
        hb_interval_sec: float = DFLT_HB_INTERVAL_SEC
    ):
        """
        Initializes the HumatronAsyncRestClient with server details and callbacks.

        Parameters:
        -----------
        server_url : str
            The server URL to send requests to.
        token : str
            Authorization token to be included in the headers.
        on_resp_payload : Callable[[ResponsePayloadPart], None]
            Callback function to handle each response payload part.
        on_hb_error : Optional[Callable[[Exception], None]]
            Optional callback function to handle errors during heartbeat.
        hb_interval_sec : float
            Interval between heartbeat requests in seconds.
        """
        self._server_url = server_url
        self._headers = _mk_headers(token)
        self._on_resp_payload = on_resp_payload
        self._on_hb_error = on_hb_error
        self._hb_interval_sec = hb_interval_sec

        self._thread = Thread(target=self._hb)
        self._stopped = False
        self._sleep_event = threading.Event()
        self._lock = threading.Lock()

    def start(self) -> None:
        """
        Starts the asynchronous client, initiating the heartbeat thread.
        """
        self._thread.start()
        _logger.info('RestClient started.')

    def close(self) -> None:
        """
        Stops the asynchronous client, terminates the heartbeat thread, and cleans up resources.
        """
        _logger.info('RestClient closing.')

        with self._lock:
            self._stopped = True
            self._sleep_event.set()

        self._thread.join()

        _logger.info('RestClient closed.')

    def post(self, req: RestRequest | RestHeartbeatRequest) -> None:
        """
        Sends a request to the server and processes the response.

        Parameters:
        -----------
        req : RestRequest | RestHeartbeatRequest
            The request to be sent.
        """
        with self._lock:
            resp = _post(self._server_url, self._headers, req)
        self._on_srv_messages(resp)

    def _on_srv_messages(self, resp: Optional[RestResponse]) -> None:
        """
        Processes the server messages by invoking the callback with each response payload part.

        Parameters:
        -----------
        resp : Optional[RestResponse]
            The response received from the server.
        """
        if resp:
            for payload in resp.payload:
                self._on_resp_payload(payload)

    def _hb(self) -> None:
        """
        The heartbeat thread function that continuously sends heartbeat requests to the server.
        """
        while True:
            with self._lock:
                if self._stopped:
                    break
                self._sleep_event.clear()

            self._sleep_event.wait(self._hb_interval_sec)

            with self._lock:
                if self._stopped:
                    break

                try:
                    resp = _post(self._server_url, self._headers, RestHeartbeatRequest.make())
                except Exception as e:
                    resp = None
                    if self._on_hb_error:
                        self._on_hb_error(e)
                    else:
                        _logger.error(f'Error during sending heartbeat [error={e}]', exc_info=True)
            self._on_srv_messages(resp)


DFLT_HB_TIMEOUT_SEC = 60


class HumatronSyncRestClient:
    """
    Synchronous REST client with heartbeat support for continuous communication.

    Attributes:
    -----------
    _server_url : str
        The server URL to send requests to.
    _headers : dict[str, str]
        HTTP headers to include in the requests.
    _hb_interval_sec : float
        Interval between heartbeat requests in seconds.

    Methods:
    --------
    post(req: RestRequest, timeout_sec: float = DFLT_HB_TIMEOUT_SEC) -> RestResponse
        Sends a request and waits for the response within the timeout period.
    """

    def __init__(
        self,
        server_url: str,
        token: str,
        hb_interval_sec: float = DFLT_HB_INTERVAL_SEC
    ):
        """
        Initializes the HumatronSyncRestClient with server details.

        Parameters:
        -----------
        server_url : str
            The server URL to send requests to.
        token : str
            Authorization token to be included in the headers.
        hb_interval_sec : float
            Interval between heartbeat requests in seconds.
        """
        self._server_url = server_url
        self._headers = _mk_headers(token)
        self._hb_interval_sec = hb_interval_sec

    def _get(self, req: RestRequest | RestHeartbeatRequest, exp_payload_id: str) -> Optional[RestResponse]:
        """
        Sends a GET request and checks if the expected payload is in the response.

        Parameters:
        -----------
        req : RestRequest | RestHeartbeatRequest
            The request to be sent.
        exp_payload_id : str
            The expected payload ID to match in the response.

        Returns:
        --------
        Optional[RestResponse]
            The response containing the expected payload, or None if not found.
        """
        resp = _post(self._server_url, self._headers, req)

        if not resp:
            return None

        for part in resp.payload:
            if part.ref_payload_id == exp_payload_id:
                return RestResponse(resp.resp_id, [part], resp.resp_tstamp)
            else:
                _logger.warning(
                    f'Unexpected response [exp_payload_id={exp_payload_id}, ref_payload_id={part.ref_payload_id}]'
                )

        return None

    def post(self, req: RestRequest, timeout_sec: float = DFLT_HB_TIMEOUT_SEC) -> RestResponse:
        """
        Sends a request and waits for the response within the specified timeout period.

        Parameters:
        -----------
        req : RestRequest
            The request to be sent.
        timeout_sec : float, optional
            The timeout period in seconds (default is DFLT_HB_TIMEOUT_SEC).

        Returns:
        --------
        RestResponse
            The response received from the server.

        Raises:
        -------
        ValueError
            If the request contains more than one payload.
        TimeoutError
            If the request times out without receiving a response.
        """
        payload = req.payload

        if len(payload) != 1:
            raise ValueError('Only single payload is supported.')

        part = payload[0]
        max_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout_sec)

        resp = self._get(req, part.payload_id)

        while not resp and datetime.datetime.now() < max_time:
            time.sleep(self._hb_interval_sec)
            resp = self._get(RestHeartbeatRequest.make(), part.payload_id)

        if not resp:
            raise TimeoutError(f'Request timed out after {timeout_sec} seconds.')

        return resp
