from http_api.http_request import http_sender
import json
import pytest


def assert_http_response(response, actual_value, error_message, expected_value=False):
    try:
        if expected_value:
            assert actual_value == expected_value, error_message
        else:
            assert len(actual_value) > 0, error_message
    except AssertionError:
        pytest.fail(response.text, error_message)


def api_sender(host, status_code, method, path, body=''):
    response, request = http_sender(host, method, path, body, {'Content-Type': 'application/x-www-form-urlencoded'})
    assert_http_response(response, response.status_code, 'Неверный статус код', status_code)
    try:
        return json.loads(response.content), request
    except UnicodeDecodeError:  # when response != json or smth
        return request
