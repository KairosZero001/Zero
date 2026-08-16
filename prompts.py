from prompt_builder import memory_schema_text


def load_prompt(name):

    with open(f"prompts/{name}", "r", encoding="utf-8") as f:
        prompt = f.read()

    if name == "memory_prompt.txt":
        prompt = prompt.replace(
            "{MEMORY_SCHEMA}",
            memory_schema_text()
        )

    return prompt
