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
import logging
from typing import NamedTuple

import flask
import werkzeug
from flask import Flask, abort, request, jsonify, make_response
from werkzeug.serving import make_server, BaseWSGIServer

from humatron.worker.classes import HumatronWorker, Request
from humatron.worker.rest_utils import check_request_token, set_response_token

_logger = logging.getLogger('humatron.sdk.flask')


class SSLContextData(NamedTuple):
    """Represents SSL context data for secure communication.

    Attributes:
        crt_path (str): The path to the SSL certificate file.
        key_path (str): The path to the SSL key file.
    """
    crt_path: str
    key_path: str


def make_flask_server(
    humatron_worker: HumatronWorker,
    req_token: str,
    resp_token: str,
    rest_host: str,
    rest_port: int,
    rest_url: str,
    methods: list[str] = None,
    ssl_ctx_data: SSLContextData = None
) -> BaseWSGIServer:
    """Creates a Flask-based HTTP server to handle requests for the HumatronWorker.

    Args:
        humatron_worker (HumatronWorker): The worker instance that handles requests.
        req_token (str): The token used to validate incoming requests.
        resp_token (str): The token to include in outgoing responses.
        rest_host (str): The host address for the server.
        rest_port (int): The port number for the server.
        rest_url (str): The URL endpoint for handling requests.
        methods (list[str], optional): HTTP methods allowed for the endpoint. Defaults to ['POST'].
        ssl_ctx_data (SSLContextData, optional): SSL context data for HTTPS. Defaults to None.

    Returns:
        BaseWSGIServer: A WSGI server instance ready to handle HTTP requests.
    """
    app = Flask(__name__)

    ssl_context = (ssl_ctx_data.crt_path, ssl_ctx_data.key_path) if ssl_ctx_data else None
    srv = make_server(rest_host, rest_port, app, ssl_context=ssl_context)

    @app.route(f'/{rest_url}', methods=methods if methods else ['POST'])
    def _process():
        """Processes incoming HTTP requests and returns a response.

        Validates the request token, processes the request using HumatronWorker,
        and sets the response token before sending the response.

        Returns:
            flask.Response: The HTTP response to be sent back to the client.
        """
        try:
            if not check_request_token(request.headers, req_token):
                abort(make_response(jsonify({}), 401))
            resp_spec = humatron_worker.post_request(Request.from_dict(request.json))
            resp_flask = flask.make_response(resp_spec.to_dict()) if resp_spec else flask.jsonify({})

            set_response_token(resp_flask.headers, resp_token)

            return resp_flask
        except werkzeug.exceptions.HTTPException as e:
            raise e
        except KeyError as e:
            abort(make_response(jsonify({'error': str(e)}), 400))
        except Exception as e:
            abort(make_response(jsonify({'error': str(e)}), 500))

    return srv


def start_flask_server(
    humatron_worker: HumatronWorker,
    req_token: str,
    resp_token: str,
    rest_host: str,
    rest_port: int,
    rest_url: str,
    methods: list[str] = None,
    ssl_ctx_data: SSLContextData = None
) -> None:
    """Starts the Flask server and handles incoming requests indefinitely.

    Args:
        humatron_worker (HumatronWorker): The worker instance that handles requests.
        req_token (str): The token used to validate incoming requests.
        resp_token (str): The token to include in outgoing responses.
        rest_host (str): The host address for the server.
        rest_port (int): The port number for the server.
        rest_url (str): The URL endpoint for handling requests.
        methods (list[str], optional): HTTP methods allowed for the endpoint. Defaults to ['POST'].
        ssl_ctx_data (SSLContextData, optional): SSL context data for HTTPS. Defaults to None.

    """
    srv = make_flask_server(
        humatron_worker, rest_host, req_token, resp_token, rest_port, rest_url, methods, ssl_ctx_data
    )

    protocol = 'http' if ssl_ctx_data is None else 'https'

    try:
        _logger.info(f'Server is running at {protocol}://{rest_host}:{rest_port}/{rest_url}')
        srv.serve_forever()
    finally:
        _logger.info('Shutting down the server.')
        humatron_worker.close()
        srv.shutdown()
