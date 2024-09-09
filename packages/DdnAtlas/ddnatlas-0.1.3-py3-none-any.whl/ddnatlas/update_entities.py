import logging
import os
from typing import Optional, List

from apache_atlas.client.base_client import AtlasClient
from apache_atlas.model.instance import AtlasEntity, AtlasEntitiesWithExtInfo, AtlasEntityWithExtInfo
from apache_atlas.utils import type_coerce

already_processed = set()


def include_element(element: str, include: Optional[List[str]], exclude: Optional[List[str]]):
    if not include and not exclude:
        return True
    elif exclude and element in exclude:
        return False
    elif include and element not in include:
        return False
    return True


def remove_nested_key(dictionary, unwanted_key):
    if isinstance(dictionary, dict):
        for key in list(dictionary.keys()):  # We use list() to avoid 'dictionary size changed during iteration' error
            if key == unwanted_key:
                del dictionary[key]
            elif isinstance(dictionary[key], dict):
                remove_nested_key(dictionary[key], unwanted_key)
            elif isinstance(dictionary[key], list):
                for item in dictionary[key]:
                    remove_nested_key(item, unwanted_key)
    return dictionary


def compare_dictionaries(dict1, dict2):
    if set(dict1.keys()) != set(dict2.keys()):
        return False

    for key, val1 in dict1.items():
        val2 = dict2[key]

        if type(val1) is not type(val2):
            return False

        if isinstance(val1, dict):
            if not compare_dictionaries(val1, val2):
                return False
        elif isinstance(val1, list):
            if sorted([str(el) for el in val1]) != sorted([str(el) for el in val2]):
                return False
        elif val1 != val2:
            return False

    return True


def deep_merge(dict1, dict2):
    merged = dict1.copy()
    for key, value in dict2.items():
        if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def update_entities(entities: Optional[List[dict]],
                    include: Optional[List[str]] = None, exclude: Optional[List[str]] = None,
                    force_updates: Optional[List[str]] = None):
    atlas_url = os.getenv('ATLAS_URL')
    username = os.getenv('ATLAS_USERNAME')
    password = os.getenv('ATLAS_PASSWORD')

    if force_updates:
        for item in force_updates:
            already_processed.remove(item)
    client = AtlasClient(atlas_url, auth=(username, password))
    for entity in entities:
        if not entity['attributes'].get('qualifiedName') in already_processed and include_element(
                entity.get('typeName'), include, exclude):
            already_processed.add(entity['attributes'].get('qualifiedName'))
            try:
                entity_type = entity['typeName']
                attribute = {'qualifiedName': entity['attributes']['qualifiedName']}.items()
                retrieved_entity = None
                try:
                    retrieved_entity = client.entity.get_entity_by_attribute(
                        type_name=entity_type,
                        uniq_attributes=attribute
                    )
                except Exception:
                    pass

                if retrieved_entity is not None:
                    entity_attributes = entity["attributes"]
                    retrieved_entity = retrieved_entity['entity']
                    retrieved_attributes = retrieved_entity.attributes
                    retrieved_selected_attributes = {k: v for k, v in retrieved_attributes.items() if
                                                     k in entity_attributes}
                    retrieved_selected_attributes = remove_nested_key(retrieved_selected_attributes, 'guid')

                    # if they are not same
                    if not compare_dictionaries(entity_attributes, retrieved_selected_attributes):
                        atlas_entity = type_coerce({"entity": entity}, AtlasEntityWithExtInfo)
                        response = client.entity.update_entity(atlas_entity)
                        logging.info({'action': 'update', 'status': response.status, 'entity': entity})
                    else:
                        logging.info({'action': 'skip', 'status': 'new entity attributes match with existing entity',
                                      'entity': entity})
                else:
                    atlas_entity = AtlasEntity({"typeName": entity.get('typeName')})
                    atlas_entity.attributes = entity.get('attributes')
                    entities_info = AtlasEntitiesWithExtInfo()
                    entities_info.entities = [atlas_entity]
                    response = client.entity.create_entities(entities_info)
                    logging.info({'action': 'create', 'status': response.status, 'entity': entity})
            except Exception as e:
                logging.error({'action': 'error', 'status': str(e), 'entity': entity})
