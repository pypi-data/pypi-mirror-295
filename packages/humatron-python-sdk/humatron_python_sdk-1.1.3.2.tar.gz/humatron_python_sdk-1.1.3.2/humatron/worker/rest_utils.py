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
from typing import Any

# REST header name for response token.
HUMATRON_RESPONSE_TOKEN = 'Humatron_Response_Token'


def check_request_token(headers: dict[str, Any], req_token: str) -> bool:
    """
    Checks if the request token in the headers matches the provided token.
    
    Args:
        headers (dict[str, Any]): The headers of the request.
        req_token (str): The request token to be checked.
    
    Returns:
        bool: True if the token matches, False otherwise.
    """
    arr = headers.get('Authorization', '').split(' ')

    return len(arr) == 2 and arr[1] == req_token


def set_response_token(headers: dict[str, Any], resp_token: str) -> None:
    """
    Sets the response token in the headers.
    
    Args:
        headers (dict[str, Any]): The headers of the response.
        resp_token (str): The response token to be set.
    """
    headers[HUMATRON_RESPONSE_TOKEN] = resp_token
