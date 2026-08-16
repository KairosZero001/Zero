from session import get_messages
from memory_search import get_relevant_memories
from memory_router import needs_memory


def memory_to_sentence(memory):
    key, value = memory.split(": ", 1)

    key = key.strip()
    value = value.strip()

    mapping = {
        "favorite_color": f"Safvan's favorite color is {value}.",
        "favorite_food": f"Safvan's favorite food is {value}.",
        "favorite_movie": f"Safvan's favorite movie is {value}.",
        "favorite_game": f"Safvan's favorite game is {value}.",
        "favorite_book": f"Safvan's favorite book is {value}.",
        "favorite_music": f"Safvan's favorite music is {value}.",
        "pet_name": f"Safvan's pet's name is {value}.",
        "dream": f"Safvan's dream is {value}.",
        "location": f"Safvan lives in {value}.",
        "profession": f"Safvan's profession is {value}.",
        "programming_language": f"Safvan's preferred programming language is {value}.",
        "editor": f"Safvan uses {value} as an editor.",
        "project": f"Safvan is working on {value}.",
    }

    return mapping.get(key, f"{key} is {value}.")


def build_context(user):
    messages = get_messages().copy()

    if not needs_memory(user):
        return messages

    relevant = get_relevant_memories(user)

    if relevant:

        memory_text = (
            "Long-term memories:\n\n"
            "The following facts are true about Safvan.\n"
            "Use them whenever they help answer the user's question.\n\n"
        )

        for item in relevant:
            memory_text += "- " + memory_to_sentence(item) + "\n"

        messages.insert(
            1,
            {
                "role": "system",
                "content": memory_text
            }
        )

    return messages