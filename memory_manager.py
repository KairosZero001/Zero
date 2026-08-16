from database import (
    save_memory,
    get_memory,
    get_all_memories,
    delete_memory
)


def remember(user):
    text = user.strip()

    if not text.lower().startswith("remember "):
        return None

    try:

        data = text[9:]

        key, value = data.split("=", 1)

        key = key.strip().lower().replace(" ", "_")

        value = value.strip()

        save_memory(
            "user",
            key,
            value,
            10
        )

        return f"I'll remember that {key} is {value}."

    except ValueError:

        return (
            "Use:\n"
            "remember favorite_color = blue"
        )


def recall(user):
    text = user.strip().lower()

    if not text.startswith("recall "):
        return None

    key = text[7:].strip().replace(" ", "_")

    value = get_memory(key)

    if value:

        return f"{key} = {value}"

    return "I don't remember that."


def forget(user):

    text = user.strip().lower()

    if not text.startswith("forget "):
        return None

    key = text[7:].strip().replace(" ", "_")

    delete_memory(key)

    return f"I forgot {key}."


def list_memories(user):

    if user.lower() not in (
        "list memories",
        "show memories",
        "show memory"
    ):
        return None

    memories = get_all_memories()

    if not memories:
        return "I don't have any memories yet."

    text = ""

    for category, key, value, importance in memories:
        text += f"{key} = {value}\n"

    return text