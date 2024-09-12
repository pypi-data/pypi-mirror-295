import re


def camel_to_title(camel_str):
    return re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', camel_str).title()
