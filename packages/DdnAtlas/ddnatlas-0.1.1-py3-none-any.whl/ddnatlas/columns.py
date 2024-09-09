def create_columns(entities, supergraph_name, subgraph_name, connector_name, collection_name, object_schema):
    column_ids = []
    for column_name, column in object_schema['fields'].items():
        nullable = column['type'].get('type') == 'nullable'
        if nullable:
            type_name = column['type']['underlying_type']['name']
        else:
            type_name = column['type']['name']
        scalar_name = f"{supergraph_name}.{subgraph_name}.{connector_name}.{type_name}"
        qualified_name = f"{supergraph_name}.{subgraph_name}.{collection_name}.{column_name}"
        column_ids.append(qualified_name)
        entities.append({
            "typeName": "column",
            "attributes": {
                "name": column_name,
                "qualifiedName": qualified_name,
                "nullable": nullable,
                "dataType": {"typeName": "scalar", "uniqueAttributes": {"qualifiedName": scalar_name}},
            }
        })
    return column_ids
