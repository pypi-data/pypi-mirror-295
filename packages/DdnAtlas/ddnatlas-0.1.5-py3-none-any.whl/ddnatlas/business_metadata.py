import os

from apache_atlas.client.base_client import AtlasClient
from ddnatlas.camel_to_title import camel_to_title


def add_business_metadata(entities, include, exclude):

    url = os.getenv('ATLAS_URL')
    username = os.getenv('ATLAS_USERNAME')
    password = os.getenv('ATLAS_PASSWORD')

    if include and 'business_metadata' not in include:
        return
    if exclude and 'business_metadata' in exclude:
        return

    client = AtlasClient(host=url, auth=(username, password))
    for entity in entities:
        if entity.get('typeName') and entity['attributes'].get('qualifiedName') and entity['attributes'].get(
                'name') and entity.get('typeName') in ["field", "column", "query", "collection", "subgraph",
                                                       "supergraph", "object_type"]:
            qualified_name = entity['attributes']['qualifiedName']
            technical_name = entity['attributes']['name']
            business_name = camel_to_title(technical_name.replace('_', ' '))
            result = client.discovery.attribute_search(type_name='Asset', attr_name='qualifiedName',
                                                       attr_value_prefix=qualified_name, limit=1, offset=0)
            guid = result['entities'][0]['guid']
            business_metadata = {
                "data_analysis": {
                    "businessNames": [business_name]
                }
            }
            try:
                client.entity.add_or_update_business_attributes(entity_guid=guid, is_overwrite=False,
                                                                business_attributes=business_metadata)
            except Exception:
                pass
