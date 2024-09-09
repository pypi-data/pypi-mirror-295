import logging
import os

from ddnatlas.execute_request import execute_request


def get_object_type(object_types, name):
    return next(item for item in object_types if item['definition']['name'] == name)


def get_entity(entities, _name, object_type):
    return next(entity for entity in entities if
                entity['typeName'] == 'object_type' and entity['attributes']['name'] ==
                object_type['definition']['graphql']['typeName'])


def get_key_ids(entity, keys):
    key_ids = []
    for key in keys:
        key_ids += [field['uniqueAttributes']['qualifiedName'] for field in entity['attributes']['fields'] if
                    field['uniqueAttributes']['qualifiedName'].endswith('.' + key)]
    return key_ids


def create_atlas_relationship(relationship, source_entity, target_entity, source_key_ids, target_key_ids):
    return {
        "typeName": "supergraph_array_relationship" if relationship['definition']['target']['model'][
                                                           'relationshipType'] != 'Object' else "supergraph_object_relationship",
        "attributes": {
            "field_name": relationship['definition']['name'],
            "source_keys": [{
                "typeName": "column",
                "uniqueAttributes": {
                    "qualifiedName": item
                }
            } for item in source_key_ids],
            "target_keys": [{
                "typeName": "column",
                "uniqueAttributes": {
                    "qualifiedName": item
                }
            } for item in target_key_ids]
        },
        "end1": {
            "typeName": "object_type",
            "uniqueAttributes": {
                "qualifiedName": source_entity['attributes']['qualifiedName']
            }
        },
        "end2": {
            "typeName": "object_type",
            "uniqueAttributes": {
                "qualifiedName": target_entity['attributes']['qualifiedName']
            }
        },
        "status": "ACTIVE"
    }


def create_relationships(relationships, object_types, entities):
    atlas_url = os.getenv('ATLAS_URL')
    username = os.getenv('ATLAS_USERNAME')
    password = os.getenv('ATLAS_PASSWORD')

    logging.info("Creating relationships..")

    for relationship in relationships:
        source_object_type = get_object_type(object_types, relationship['definition']['sourceType'])
        target_object_type = get_object_type(object_types,
                                             relationship['definition']['target']['model']['name'])

        source_entity = get_entity(entities, source_object_type['definition']['graphql']['typeName'],
                                   source_object_type)
        target_entity = get_entity(entities, target_object_type['definition']['graphql']['typeName'],
                                   target_object_type)

        source_keys = ['.'.join(item['fieldName'] for item in mapping['source']['fieldPath']) for mapping in
                       relationship['definition']['mapping']]
        target_keys = ['.'.join(item['fieldName'] for item in mapping['target']['modelField']) for mapping in
                       relationship['definition']['mapping']]

        source_key_ids = get_key_ids(source_entity, source_keys)
        target_key_ids = get_key_ids(source_entity, target_keys)

        atlas_relationship = create_atlas_relationship(relationship, source_entity, target_entity, source_key_ids,
                                                       target_key_ids)
        execute_relationship_request(atlas_url, username, password, atlas_relationship)
    supergraph = [item for item in entities if item.get('typeName') == 'supergraph'][0]
    for entity in entities:
        if entity['typeName'] == 'field':
            rel = {
                "typeName": "data_source_to_api",
                "attributes": {
                    "transform": f"{supergraph['attributes'].get('name', 'enterprise')}.straight_through"
                },
                "end1": {
                    "typeName": "column",
                    "uniqueAttributes": {
                        "qualifiedName": entity['attributes']['column']['uniqueAttributes']['qualifiedName']
                    }
                },
                "end2": {
                    "typeName": "field",
                    "uniqueAttributes": {
                        "qualifiedName": entity['attributes']['qualifiedName']
                    }
                },
                "status": "ACTIVE"
            }
            execute_relationship_request(atlas_url, username, password, rel)
        if entity['typeName'] == 'collection':
            for column in entity['attributes']['columns']:
                rel = {
                    "typeName": "collection_owns_column",
                    "attributes": {
                        "description": f"{entity['attributes']['qualifiedName']} has the column: {column['uniqueAttributes']['qualifiedName']}"
                    },
                    "end1": {
                        "typeName": "collection",
                        "uniqueAttributes": {
                            "qualifiedName": entity['attributes']['qualifiedName']
                        }
                    },
                    "end2": {
                        "typeName": "column",
                        "uniqueAttributes": {
                            "qualifiedName": column['uniqueAttributes']['qualifiedName']
                        }
                    },
                    "status": "ACTIVE"
                }
                execute_relationship_request(atlas_url, username, password, rel)
        if entity['typeName'] == 'object_type':
            for field in entity['attributes']['fields']:
                rel = {
                    "typeName": "object_type_owns_field",
                    "attributes": {
                        "description": f"{entity['attributes']['qualifiedName']} has the field: {field['uniqueAttributes']['qualifiedName']}"
                    },
                    "end1": {
                        "typeName": "object_type",
                        "uniqueAttributes": {
                            "qualifiedName": entity['attributes']['qualifiedName']
                        }
                    },
                    "end2": {
                        "typeName": "field",
                        "uniqueAttributes": {
                            "qualifiedName": field['uniqueAttributes']['qualifiedName']
                        }
                    },
                    "status": "ACTIVE"
                }
                execute_relationship_request(atlas_url, username, password, rel)
        if entity['typeName'] == 'data_connector':
            for collection in entity['attributes']['collections']:
                rel = {
                    "typeName": "data_connector_has_collection",
                    "attributes": {
                        "description": f"{entity['attributes']['qualifiedName']} has the collection: {collection['uniqueAttributes']['qualifiedName']}"
                    },
                    "end1": {
                        "typeName": "data_connector",
                        "uniqueAttributes": {
                            "qualifiedName": entity['attributes']['qualifiedName']
                        }
                    },
                    "end2": {
                        "typeName": "collection",
                        "uniqueAttributes": {
                            "qualifiedName": collection['uniqueAttributes']['qualifiedName']
                        }
                    },
                    "status": "ACTIVE"
                }
                execute_relationship_request(atlas_url, username, password, rel)
        if entity['typeName'] == 'supergraph':
            for subgraph in entity['attributes']['domains']:
                rel = {
                    "typeName": "supergraph_has_subgraph",
                    "attributes": {
                        "description": f"{entity['attributes']['qualifiedName']} has the collection: {subgraph['uniqueAttributes']['qualifiedName']}"
                    },
                    "end1": {
                        "typeName": "supergraph",
                        "uniqueAttributes": {
                            "qualifiedName": entity['attributes']['qualifiedName']
                        }
                    },
                    "end2": {
                        "typeName": "subgraph",
                        "uniqueAttributes": {
                            "qualifiedName": subgraph['uniqueAttributes']['qualifiedName']
                        }
                    },
                    "status": "ACTIVE"
                }
                execute_relationship_request(atlas_url, username, password, rel)
        if entity['typeName'] == 'subgraph':
            for data_connector in entity['attributes']['data_connectors']:
                rel = {
                    "typeName": "subgraph_has_data_connector",
                    "attributes": {
                        "description": f"{entity['attributes']['qualifiedName']} has the collection: {data_connector['uniqueAttributes']['qualifiedName']}"
                    },
                    "end1": {
                        "typeName": "subgraph",
                        "uniqueAttributes": {
                            "qualifiedName": entity['attributes']['qualifiedName']
                        }
                    },
                    "end2": {
                        "typeName": "data_connector",
                        "uniqueAttributes": {
                            "qualifiedName": data_connector['uniqueAttributes']['qualifiedName']
                        }
                    },
                    "status": "ACTIVE"
                }
                execute_relationship_request(atlas_url, username, password, rel)
            for query in entity['attributes']['queries']:
                rel = {
                    "typeName": "subgraph_has_query",
                    "attributes": {
                        "description": f"{entity['attributes']['qualifiedName']} has the collection: {query['uniqueAttributes']['qualifiedName']}"
                    },
                    "end1": {
                        "typeName": "subgraph",
                        "uniqueAttributes": {
                            "qualifiedName": entity['attributes']['qualifiedName']
                        }
                    },
                    "end2": {
                        "typeName": "query",
                        "uniqueAttributes": {
                            "qualifiedName": query['uniqueAttributes']['qualifiedName']
                        }
                    },
                    "status": "ACTIVE"
                }
                execute_relationship_request(atlas_url, username, password, rel)
            for mutation in entity['attributes']['mutations']:
                rel = {
                    "typeName": "subgraph_has_mutation",
                    "attributes": {
                        "description": f"{entity['attributes']['qualifiedName']} has the collection: {mutation['uniqueAttributes']['qualifiedName']}"
                    },
                    "end1": {
                        "typeName": "subgraph",
                        "uniqueAttributes": {
                            "qualifiedName": entity['attributes']['qualifiedName']
                        }
                    },
                    "end2": {
                        "typeName": "mutation",
                        "uniqueAttributes": {
                            "qualifiedName": mutation['uniqueAttributes']['qualifiedName']
                        }
                    },
                    "status": "ACTIVE"
                }
                execute_relationship_request(atlas_url, username, password, rel)
            for object_type in entity['attributes']['subgraph_schema']:
                rel = {
                    "typeName": "subgraph_has_object_type",
                    "attributes": {
                        "description": f"{entity['attributes']['qualifiedName']} has the object_type: {object_type['uniqueAttributes']['qualifiedName']}"
                    },
                    "end1": {
                        "typeName": "subgraph",
                        "uniqueAttributes": {
                            "qualifiedName": entity['attributes']['qualifiedName']
                        }
                    },
                    "end2": {
                        "typeName": "object_type",
                        "uniqueAttributes": {
                            "qualifiedName": object_type['uniqueAttributes']['qualifiedName']
                        }
                    },
                    "status": "ACTIVE"
                }
                execute_relationship_request(atlas_url, username, password, rel)
        if entity['typeName'] == 'query':
            object_type = entity['attributes']['record']
            rel = {
                "typeName": "query_has_object_type",
                "attributes": {
                    "description": f"{entity['attributes']['qualifiedName']} has the collection: {object_type['uniqueAttributes']['qualifiedName']}"
                },
                "end1": {
                    "typeName": "query",
                    "uniqueAttributes": {
                        "qualifiedName": entity['attributes']['qualifiedName']
                    }
                },
                "end2": {
                    "typeName": "object_type",
                    "uniqueAttributes": {
                        "qualifiedName": object_type['uniqueAttributes']['qualifiedName']
                    }
                },
                "status": "ACTIVE"
            }
            execute_relationship_request(atlas_url, username, password, rel)


def execute_relationship_request(atlas_url, username, password, atlas_relationship):
    logging.info("Executing relationship request..")
    response = execute_request('post', f"{atlas_url}/api/atlas/v2/relationship", json_data=atlas_relationship,
                               username=username, password=password)
    if response.status_code not in (200, 409):
        raise Exception(response.text)
