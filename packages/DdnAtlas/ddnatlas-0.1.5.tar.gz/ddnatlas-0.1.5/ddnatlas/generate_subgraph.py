from ddnatlas.connector_collections import create_collection
from ddnatlas.columns import create_columns
from ddnatlas.data_connectors import create_data_connector
from ddnatlas.fields import create_fields
from ddnatlas.object_types import get_object_type_and_name, create_object_type
from ddnatlas.queries import create_queries
from ddnatlas.scalars import create_scalars
from ddnatlas.update_entities import update_entities
import logging


def generate_subgraph(supergraph, subgraph, connectors, data_connector_links,
                      object_types, models, include, exclude):
    logging.info('Starting to generate subgraph...')

    supergraph_name = supergraph['definition'].get('name', 'enterprise')
    subgraph_name = subgraph['definition']['name']
    subgraph_data_connectors = [item for item in connectors if item['definition']['subgraph'] == subgraph_name]
    entities = []
    data_connector_ids = []
    object_type_ids = []
    query_ids = []
    for subgraph_data_connector in subgraph_data_connectors:
        logging.info('Processing subgraph data connectors...')
        connector_name = subgraph_data_connector['definition']['name']
        link = [item for item in data_connector_links if item['definition']['name'] == connector_name][0]
        subgraph_data_connector['schema'] = link['definition']['schema']['schema']
        # CREATE SCALARS
        logging.info('Creating scalars...')
        scalar_ids = create_scalars(entities, supergraph_name, subgraph_name, connector_name, subgraph_data_connector)
        logging.info('Finished creating scalars. Total created: %d', len(scalar_ids))
        update_entities(entities, include, exclude)
        collection_ids = []
        for collection_name, object_schema in subgraph_data_connector['schema']['object_types'].items():
            # CREATE COLUMNS
            logging.info('Creating columns...')
            column_ids = create_columns(entities, supergraph_name, subgraph_name, connector_name, collection_name,
                                        object_schema)
            logging.info('Finished creating columns. Total created: %d', len(column_ids))
            update_entities(entities, include, exclude)
            # CREATE FIELDS
            logging.info('Creating fields...')
            object_type, object_name = get_object_type_and_name(object_types, connector_name, collection_name)
            field_ids = create_fields(supergraph_name, subgraph_name, object_name, object_type, entities)
            logging.info('Finished creating fields. Total created: %d', len(field_ids))
            update_entities(entities, include, exclude)
            # CREATE COLLECTION
            logging.info('Creating collections...')
            collection_ids.append(
                create_collection(subgraph_data_connector, collection_name, supergraph_name, subgraph_name, column_ids,
                                  entities))
            logging.info('Finished creating collections. Total created: %d', len(collection_ids))
            update_entities(entities, include, exclude)
            # CREATE OBJECT_TYPE
            logging.info('Creating object types...')
            object_qualified_name = create_object_type(supergraph_name, subgraph_name, object_name, field_ids, entities)
            object_type_ids.append(object_qualified_name)
            logging.info('Finished creating object types. Total created: %d', len(object_type_ids))
            update_entities(entities, include, exclude)
            # CREATE QUERIES
            logging.info('Creating queries...')
            data_connector_model = [item for item in models if
                                    item['definition']['source']['dataConnectorName'] == connector_name and
                                    item['definition']['source']['collection'] == collection_name][0]
            query_ids = query_ids + create_queries(supergraph_name, subgraph_name, object_qualified_name,
                                                   data_connector_model, entities)
            logging.info('Finished creating queries. Total created: %d', len(query_ids))
            update_entities(entities, include, exclude)
        # CREATE DATA CONNECTORS
        logging.info('Creating data connectors...')
        data_connector_ids.append(
            create_data_connector(supergraph_name, subgraph_name, connector_name, subgraph_data_connector, scalar_ids,
                                  collection_ids, entities))
        logging.info('Finished creating data connectors. Total created: %d', len(data_connector_ids))
        update_entities(entities, include, exclude)
    entities.append({
        "typeName": "subgraph",
        "attributes": {
            "qualifiedName": f"{supergraph_name}.{subgraph_name}",
            "name": subgraph_name,
            "queries": [{"typeName": "query", "uniqueAttributes": {"qualifiedName": item}} for item in
                        query_ids],
            "mutations": [],
            "data_connectors": [{"typeName": "data_connector", "uniqueAttributes": {"qualifiedName": item}} for item in
                                data_connector_ids],
            "subgraph_schema": [{"typeName": "object_type", "uniqueAttributes": {"qualifiedName": item}} for item in
                                object_type_ids]
        }
    })
    update_entities(entities, include, exclude)
    logging.info('Finished generating subgraph...')
    return entities
