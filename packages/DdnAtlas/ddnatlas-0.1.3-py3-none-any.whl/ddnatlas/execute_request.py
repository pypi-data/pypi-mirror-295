import requests
import logging
from requests.auth import HTTPBasicAuth


def execute_request(http_method, url, headers={}, params=None, json_data=None, username=None, password=None):
    auth = None
    if username and password:
        auth = HTTPBasicAuth(username, password)

    try:
        if http_method == "get":
            logging.info('Sending GET request to %s', url)
            response = requests.get(url, params=params, headers=headers, auth=auth)
        elif http_method == "post":
            logging.info('Sending POST request to %s', url)
            response = requests.post(url, params=params, headers=headers, json=json_data, auth=auth)
        elif http_method == "delete":
            logging.info('Sending DELETE request to %s', url)
            response = requests.delete(url, params=params, headers=headers, auth=auth)
        elif http_method == "put":
            logging.info('Sending PUT request to %s', url)
            response = requests.put(url, params=params, headers=headers, json=json_data, auth=auth)
        else:
            return None

        logging.info('Response status code: %d', response.status_code)
        return response

    except Exception:
        logging.error('Exception occurred', exc_info=True)
