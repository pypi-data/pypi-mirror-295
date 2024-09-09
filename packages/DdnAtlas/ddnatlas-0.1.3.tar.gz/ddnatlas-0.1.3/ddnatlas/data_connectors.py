def create_data_connector(supergraph_name, subgraph_name, connector_name, subgraph_data_connector, scalar_ids,
                          collection_ids, entities):
    qualified_name = f"{supergraph_name}.{subgraph_name}.{connector_name}"
    entities.append({
        "typeName": "data_connector",
        "attributes": {
            "qualifiedName": qualified_name,
            "name": connector_name,
            "subgraph": subgraph_data_connector['definition']['subgraph'],
            "source": subgraph_data_connector['definition']['source'],
            "env_mapping": subgraph_data_connector['definition']['envMapping'],
            "scalar_types": [{"typeName": "scalar", "uniqueAttributes": {"qualifiedName": item}} for item in
                             scalar_ids],
            "functions": [item.get('name') for item in subgraph_data_connector['schema']['functions']],
            "procedures": [item.get('name') for item in subgraph_data_connector['schema']['procedures']],
            "collections": [{"typeName": "collection", "uniqueAttributes": {"qualifiedName": item}} for item in
                            collection_ids],
        }
    })
    return qualified_name
