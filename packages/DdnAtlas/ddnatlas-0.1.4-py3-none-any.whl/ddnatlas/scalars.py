def create_scalars(entities, supergraph_name, subgraph_name, connector_name, subgraph_data_connector):
    scalar_ids = []
    for scalar_name, scalar in subgraph_data_connector['schema']['scalar_types'].items():
        qualified_name = f"{supergraph_name}.{subgraph_name}.{connector_name}.{scalar_name}"
        scalar_ids.append(qualified_name)
        entities.append({
            "typeName": "scalar",
            "attributes": {
                "name": scalar_name,
                "representation": scalar['representation']['type'],
                "aggregate_functions": list(scalar['aggregate_functions'].keys()),
                "comparison_operators": list(scalar['comparison_operators'].keys()),
                "qualifiedName": qualified_name
            }
        })
    return scalar_ids
