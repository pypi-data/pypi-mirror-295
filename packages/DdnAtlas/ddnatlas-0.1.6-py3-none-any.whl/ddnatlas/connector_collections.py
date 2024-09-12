def get_collection(subgraph_data_connector, collection_name):
    collection = [item for item in subgraph_data_connector['schema']['collections'] if item['name'] == collection_name][
        0]
    return collection


def create_collection(subgraph_data_connector, collection_name, supergraph_name, subgraph_name, column_ids, entities):
    collection = get_collection(subgraph_data_connector, collection_name)
    qualified_name = f"{supergraph_name}.{subgraph_name}.{collection_name}"

    entities.append({
        "typeName": "collection",
        "attributes": {
            "name": collection_name,
            "qualifiedName": qualified_name,
            "primary_keys": list(collection['uniqueness_constraints']['PK']['unique_columns']),
            "columns": [{"typeName": "column", "uniqueAttributes": {"qualifiedName": item}} for item in
                        column_ids]
        }
    })

    return qualified_name
