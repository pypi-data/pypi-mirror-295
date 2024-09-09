import os

from ddnatlas.execute_request import execute_request


def get_entities():
    atlas_url = os.getenv('ATLAS_URL')
    username = os.getenv('ATLAS_USERNAME')
    password = os.getenv('ATLAS_PASSWORD')
    response = execute_request("get", f"{atlas_url}/api/atlas/v2/search/dsl?limit=1000&offset=0&typeName=Asset",
                               username=username, password=password).json()
    return response['entities']

