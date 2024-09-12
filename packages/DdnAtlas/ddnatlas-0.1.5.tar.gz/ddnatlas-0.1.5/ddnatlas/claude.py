import json
import os
import anthropic


def process_json_with_claude(prompt, api_key=None):
    client = anthropic.Client(api_key=api_key)
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=8192,
        temperature=0,
        system="""You are a world-class data scientist at a Fortune 500 company specializing in data governance and 
        metadata management. Always respond with valid JSON objects. Each response should be a single JSON object 
        containing the requested information. Do not include any text outside of the JSON object in your response.""",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    """
    Process a JSON structure using the Claude 3.5 Sonnet API and return a JSON structure.
    :param input_json: Dict or JSON-serializable object to be processed
    :param prompt: String containing the prompt for Claude
    :param api_key: Optional API key. If not provided, it will be read from the ANTHROPIC_API_KEY environment variable
    :return: Processed JSON structure
    """
    if api_key is None:
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if api_key is None:
            raise ValueError("API key not provided and ANTHROPIC_API_KEY environment variable not set")

    try:
        full_response = ''.join(block.text for block in message.content)
        return json.loads(full_response)
    except anthropic.AnthropicError as e:
        raise Exception(f"API request failed with status code {e}")
    except json.JSONDecodeError:
        raise ValueError("The API response could not be parsed as JSON")
