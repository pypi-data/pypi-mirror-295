import json
import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError, RequestException


def headers(access_token: str = None):
    return {
        'Authorization': f'Bearer {access_token}',
        'accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded'
    }


def make_post_request(url, data, request_headers):
    try:
        response = requests.post(url=url, data=data, headers=request_headers)
        response.raise_for_status()
        return response.json()
    except ConnectionError as ce:
        return f'Connection Error: {ce}'
    except Timeout as te:
        return f'Request Timeout: {te}'
    except HTTPError as he:
        return f'HTTP Error: {he}'
    except RequestException as re:
        return f'Request Exception: {re}'
    except json.JSONDecodeError as je:
        return f'JSON Decode Error: {je}'


def make_get_request(url, data, request_headers):
    try:
        response = requests.get(url=url, data=data, headers=request_headers)
        response.raise_for_status()
        return response.json()
    except ConnectionError as ce:
        return f'Connection Error: {ce}'
    except Timeout as te:
        return f'Request Timeout: {te}'
    except HTTPError as he:
        return f'HTTP Error: {he}'
    except RequestException as re:
        return f'Request Exception: {re}'
    except json.JSONDecodeError as je:
        return f'JSON Decode Error: {je}'
