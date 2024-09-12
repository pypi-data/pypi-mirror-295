import json
import os

from ddnatlas.claude import process_json_with_claude
from ddnatlas.get_entities import get_entities

descriptions_prompt = """This is an array of Apache Atlas entities: {{entities}}. For each entity generate a 
description based on the entity's metadata and it's context.

Add an entry to a dictionary where the key is the "qualifiedName" of the entity and the value is the derived 
description. In this format:

{ "<entity qualified name">: "<description>" }
"""


def add_descriptions(entities, include, exclude):
    api_key = os.environ["ANTHROPIC_API_KEY"]

    if include and 'descriptions' not in include:
        return
    if exclude and 'descriptions' in exclude:
        return
    if not api_key:
        return

    existing_entities = get_entities()
    updated_entities = []
    missing_descriptions = [item for item in existing_entities if
                            item['attributes'].get("description") is None or item['attributes'].get(
                                'description') == ""]
    new_descriptions = process_json_with_claude(
        descriptions_prompt.replace('{{entities}}', json.dumps(missing_descriptions)),
        api_key
    )
    for key, description in new_descriptions.items():
        for entity in entities:
            if entity["attributes"]["qualifiedName"] == key:
                entity["attributes"]["description"] = description
                updated_entities.append(entity['attributes'].get('qualifiedName'))
    return updated_entities
