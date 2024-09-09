def get_object_type_and_name(object_types, connector_name, collection_name):
    object_type = [item for item in object_types if any(
        obj.get('dataConnectorName') == connector_name and obj.get('dataConnectorObjectType') == collection_name
        for obj in item['definition']['dataConnectorTypeMapping'])][0]
    object_name = object_type['definition']['graphql']['typeName']

    return object_type, object_name


def create_object_type(supergraph_name, subgraph_name, object_name, field_ids, entities):
    object_qualified_name = "{}.{}.{}".format(supergraph_name, subgraph_name, object_name)
    object_type_info = {
        "typeName": "object_type",
        "attributes": {
            "name": object_name,
            "qualifiedName": object_qualified_name,
            "fields": [{
                "typeName": "field",
                "uniqueAttributes": {
                    "qualifiedName": item
                }
            } for item in field_ids]
        }
    }
    entities.append(object_type_info)
    return object_qualified_name
