def create_queries(supergraph_name, subgraph_name, object_qualified_name, data_connector_model, entities):
    query_ids = []
    select = data_connector_model['definition']['graphql'].get('selectMany').get('queryRootField')
    qualified_name = f'{supergraph_name}.{subgraph_name}.{select}'
    entities.append({
        "typeName": "query",
        "attributes": {
            "name": select,
            "qualifiedName": qualified_name,
            "is_array": True,
            "unique_identifiers": [],
            "record": {
                "typeName": "object_type",
                "uniqueAttributes": {
                    "qualifiedName": object_qualified_name
                }
            }
        }
    })
    query_ids.append(qualified_name)
    select_uniques = [item for item in data_connector_model['definition']['graphql'].get('selectUniques')]
    for selectUnique in select_uniques:
        qualified_name = f'{supergraph_name}.{subgraph_name}.{selectUnique["queryRootField"]}'
        entities.append({
            "typeName": "query",
            "attributes": {
                "name": selectUnique["queryRootField"],
                "qualifiedName": qualified_name,
                "is_array": False,
                "unique_identifiers": selectUnique["uniqueIdentifier"],
                "record": {
                    "typeName": "object_type",
                    "uniqueAttributes": {
                        "qualifiedName": object_qualified_name
                    }
                }
            }
        })
        query_ids.append(qualified_name)
    return query_ids
