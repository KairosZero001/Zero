from memory_schema import MEMORY_SCHEMA


def memory_schema_text():

    text = ""

    for key, info in MEMORY_SCHEMA.items():
        text += f"{key} - {info['description']}\n"

    return text