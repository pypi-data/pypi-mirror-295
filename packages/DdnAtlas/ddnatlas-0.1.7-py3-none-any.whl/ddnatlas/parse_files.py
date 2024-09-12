import os
from typing import List, Dict, Any
import logging
import yaml


def parse_files(directory: str) -> List[Dict[str, Any]]:
    parsed_data = []
    logging.info(f"Searching for files in: {os.path.abspath(directory)}")
    for root, dirs, files in os.walk(directory):
        logging.info(f"Current directory: {root}")
        logging.info(f"Subdirectories: {dirs}")
        logging.info(f"Files: {files}")
        for file in files:
            if file.endswith(('.hml', '.yml', '.yaml')):
                file_path = os.path.join(root, file)
                logging.info(f"Processing file: {file_path}")
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        if content.startswith('---'):
                            # Multi-document YAML file
                            docs = yaml.safe_load_all(content)
                            parsed_data.extend(list(docs))
                        else:
                            # Single YAML document
                            parsed_data.append(yaml.safe_load(content))
                    logging.info(f"Successfully parsed: {file_path}")
                except Exception as e:
                    logging.error(f"Error processing {file_path}: {e}")

    logging.info(f"Total parsed documents: {len(parsed_data)}")
    return parsed_data
