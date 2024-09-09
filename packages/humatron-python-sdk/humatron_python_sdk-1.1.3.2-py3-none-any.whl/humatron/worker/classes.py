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
import os
import threading
import uuid
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, NamedTuple, Any, Union

from locked_dict.locked_dict import LockedDict

PayloadPart = dict[Any, Any]
Storage = dict[Any, Any]


class Request(NamedTuple):
    """
    Represents a request with command, ID, timestamp, payload, and optional storage.

    Attributes:
        req_cmd (str): The command associated with the request.
        req_id (str): The unique identifier for the request.
        req_tstamp (datetime): The timestamp of the request.
        payload (list[PayloadPart]): A list of payload parts associated with the request.
        storage (Optional[Storage]): An optional storage dictionary that can be used during processing.
    """

    req_cmd: str
    req_id: str
    req_tstamp: str
    payload: list[PayloadPart]
    storage: Optional[Storage]

    @classmethod
    def make(cls, cmd: str, payload: list[PayloadPart] | PayloadPart, storage: Optional[Storage] = None) -> 'Request':
        p = payload if isinstance(payload, list) else [payload]
        return cls(cmd, str(uuid.uuid4()), _utc_now_iso_format(), p, storage)

    @classmethod
    def from_json(cls, js: str):
        """
        Creates a Request instance from a JSON string.

        Args:
            js (str): The JSON string representing the request.

        Returns:
            Request: A new instance of the Request class.
        """
        return cls.from_dict(json.loads(js))

    @classmethod
    def from_dict(cls, d: dict[Any, Any]):
        """
        Creates a Request instance from a dictionary.

        Args:
            d (dict[Any, Any]): The dictionary representing the request.

        Returns:
            Request: A new instance of the Request class.
        """
        return cls(d['req_cmd'], d['req_id'], d['req_tstamp'], d['payload'], d.get('storage'))

    def to_json(self) -> str:
        """
        Converts the Request instance to a JSON string.

        Returns:
            str: The JSON string representation of the request.
        """
        return json.dumps(self.to_dict())

    def to_dict(self) -> dict[Any, Any]:
        """
        Converts the Request instance to a dictionary.

        Returns:
            dict[Any, Any]: The dictionary representation of the request.
        """
        return {
            'req_cmd': self.req_cmd,
            'req_id': self.req_id,
            'req_tstamp': self.req_tstamp,
            'payload': self.payload,
            'storage': self.storage
        }


class Response(NamedTuple):
    """
    Represents a response with ID, timestamp, optional payload, and optional storage.

    Attributes:
        resp_id (str): The unique identifier for the response.
        resp_tstamp (datetime): The timestamp of the response.
        payload (Optional[list[PayloadPart]]): An optional list of payload parts associated with the response.
        storage (Optional[Storage]): An optional storage dictionary that can be used during processing.
    """

    resp_id: str
    resp_tstamp: str
    payload: Optional[list[PayloadPart]]
    storage: Optional[Storage]

    @classmethod
    def from_json(cls, js: str):
        """
        Creates a Response instance from a JSON string.

        Args:
            js (str): The JSON string representing the response.

        Returns:
            Response: A new instance of the Response class.
        """
        return cls.from_dict(json.loads(js))

    @classmethod
    def from_dict(cls, d: dict[Any, Any]):
        """
        Creates a Response instance from a dictionary.

        Args:
            d (dict[Any, Any]): The dictionary representing the response.

        Returns:
            Response: A new instance of the Response class.
        """

        return cls(
            d['resp_id'], d['resp_tstamp'], _get_opt(d, 'payload'), _get_opt(d, 'storage')
        )

    def to_json(self) -> str:
        """
        Converts the Response instance to a JSON string.

        Returns:
            str: The JSON string representation of the response.
        """
        return json.dumps(self.to_dict())

    def to_dict(self) -> dict[Any, Any]:
        """
        Converts the Response instance to a dictionary.

        Returns:
            dict[Any, Any]: The dictionary representation of the response.
        """
        return {
            'resp_id': self.resp_id,
            'resp_tstamp': self.resp_tstamp,
            'payload': self.payload,
            'storage': self.storage
        }


logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
_logger = logging.getLogger('humatron.worker.sdk')


class HumatronWorker(ABC):
    """
    Abstract base class for a Humatron worker.

    This class defines the interface that must be implemented by any concrete Humatron worker.
    """

    @abstractmethod
    def post_request(self, req: Request) -> Optional[Response]:
        """
        Abstract method to post a request and optionally return a response.

        Args:
            req (Request): The request to be processed.

        Returns:
            Optional[Response]: The response after processing the request, if any.
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Abstract method to close the specialist resources.

        This method is responsible for cleaning up any resources used by the worker.
        """
        pass


class RequestPayloadPart(NamedTuple):
    """
    Represents a part of the request payload with command, ID, timestamp, and payload part.

    Attributes:
        req_cmd (str): The command associated with the payload part.
        req_id (str): The unique identifier for the request.
        req_tstamp (datetime): The timestamp of the request.
        payload_part (PayloadPart): A dictionary representing a part of the request payload.
    """

    req_cmd: str
    req_id: str
    req_tstamp: str
    payload_part: PayloadPart


ResponsePayloadPart = Union[list[PayloadPart], PayloadPart, None]


class HumatronWorkerAsyncAdapter(HumatronWorker, ABC):
    """
    Asynchronous adapter for Humatron worker using a thread pool executor.

    This class extends the HumatronWorker to provide asynchronous request processing
    using a thread pool.
    """

    def __init__(self, pool_size: Optional[int] = None):
        """
        Initializes the async adapter with a thread pool.

        Args:
            pool_size (Optional[int]): The maximum number of threads in the pool.
                                        Defaults to the number of CPUs if not provided.
        """
        super().__init__()
        self._pool = ThreadPoolExecutor(max_workers=pool_size if pool_size else os.cpu_count())
        self._payloads_parts: list[PayloadPart] = []
        self._lock = threading.Lock()
        self._storage: Optional[LockedDict] = None

    def close(self):
        """
        Shuts down the thread pool.

        This method ensures that all running tasks are completed before shutting down the pool.
        """
        self._pool.shutdown()

    def post_request(self, req: Request) -> Optional[Response]:
        """
        Posts a request asynchronously, processing payload parts and returning a response.

        Args:
            req (Request): The request to be processed.

        Returns:
            Optional[Response]: The response after processing the request, if any.
        """
        if req.req_cmd == 'interview':
            if req.storage:
                raise ValueError('Storage cannot be provided for `interview` requests.')
            elif not req.payload or len(req.payload) != 1:
                raise ValueError('Invalid payload for `interview` request.')

            pp = self.execute(RequestPayloadPart(req.req_cmd, req.req_id, req.req_tstamp, req.payload[0]), None)

            match pp:
                case dict():
                    return Response(make_id(), _utc_now_iso_format(), [pp], None)
                case _:
                    raise ValueError(f'Unexpected response payload for `interview` request [payload={pp}]')

        if self._storage is None:
            self._storage = LockedDict()
            self._storage.update(req.storage)

        def fn():
            try:
                res: list[PayloadPart] = []
                if req.payload:
                    for parts in req.payload:
                        parts = self.execute(
                            RequestPayloadPart(req.req_cmd, req.req_id, req.req_tstamp, parts), self._storage
                        )

                        if parts is not None:
                            if not isinstance(parts, list):
                                parts = [parts]

                            parts = list(filter(lambda el: el, parts)) if parts else None

                            if parts:
                                res.extend(parts)
                    with self._lock:
                        if res:
                            self._payloads_parts.extend(res)
            except Exception as e:
                _logger.error(f'Error during processing [error={e}]', exc_info=True)

        self._pool.submit(fn)

        with self._lock:
            if not self._payloads_parts and not self._storage:
                return None

            payloads = self._payloads_parts[:]
            self._payloads_parts.clear()

        return Response(
            make_id(),
            _utc_now_iso_format(),
            (payloads if payloads else None),
            self._storage.copy()
        )

    @abstractmethod
    def execute(self, req: RequestPayloadPart, storage: Optional[Storage]) -> ResponsePayloadPart:
        """
        Abstract method to execute a request payload part.

        Args:
            req (RequestPayloadPart): The request payload part to be executed.
            storage (Storage): The storage dictionary used for processing.

        Returns:
            ResponsePayloadPart: The result of the execution, which could be a list of payload parts,
                                 a single payload part, or None.
        """
        pass


def _get_opt(d: dict[str, Any], k: str) -> Optional[Any]:
    """
    Gets an optional value from a dictionary by key.

    Args:
        d (dict[str, Any]): The dictionary from which to retrieve the value.
        k (str): The key to look up in the dictionary.

    Returns:
        Optional

    [Any]: The value associated with the key, or None if the key is not present.
    """
    return d.get(k)


def _utc_now_iso_format() -> str:
    """
    Returns the current UTC time in ISO format.

    Returns:
    --------
    str
        The current UTC time in ISO format, truncated to milliseconds.
    """
    return f'{datetime.datetime.utcnow().isoformat()[:-3]}Z'


def make_id() -> str:
    """
    Generates a unique ID.

    Returns:
        str: A unique identifier as a string.
    """
    return str(uuid.uuid4().hex)


def make_default_response_payload(
    req_cmd: str,
    req_payload_part: PayloadPart,
    contacts: Optional[list[dict[str, Any]]] = None
) -> Optional[PayloadPart]:
    instance = req_payload_part['instance']

    def mk_response(extra: Optional[PayloadPart] = None) -> PayloadPart:
        d = {
            'resp_cmd': req_cmd,
            'instance_id': instance['id'],
            'ref_payload_id': req_payload_part['payload_id']
        }

        if contacts:
            d['contacts'] = contacts
        if extra:
            d.update(extra)
        return d

    match req_cmd:
        case 'register' | 'pause' | 'resume':
            return mk_response({'result': True})
        case 'unregister':
            return mk_response()
        case 'heartbeat':
            return None
        case _:
            raise ValueError(f'Unsupported request type: {req_cmd}')


def extract_channel_type(
    resources: list[dict[str, Any]],
    res_id: int,
    supported: set[str] = None
) -> str:
    channel_type = next((r['channel_type'] for r in resources if r['id'] == res_id), None)

    if not channel_type:
        raise ValueError(f'Unexpected resource: {res_id}')
    elif supported is not None and channel_type not in supported:
        raise ValueError(f'Unsupported channel type: {channel_type}')

    return channel_type
