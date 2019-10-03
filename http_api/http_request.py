from requests import Request, Session
import pytest


def __print_request(req):
    return ('{}\r\n{}\r\n\r\n{}'.format(
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.json,
    ))  # req toolbelt is better


def http_sender(host, method, path, body, headers):
    response = None
    request = None
    session = Session()

    if path == '':
        url = host
    else:
        url = host + path

    try:
        request = Request(method=method, url=url, json=body, headers=headers)
        prepared = session.prepare_request(request)
        response = session.send(prepared, timeout=0.5)
    except ConnectionError:
        pytest.fail('-----------FAILED REQUEST-----------\n' + __print_request(request))
    except TimeoutError:
        pytest.fail('-----------TIMEOUT REQUEST-----------\n' + __print_request(request))

    session.close()
    return response, __print_request(request)
