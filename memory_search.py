import json
import re

from memory_score import memory_score
from database import get_all_memories
from models import MODELS
from ollama import normal_chat
from prompts import load_prompt
from keyword_search import search_by_keywords, broad_question_check
from memory_schema import(
    aliases_of,
    resolve_key
)

def get_relevant_memories(user):

    memories = get_all_memories()

    # Broad questions
    results = broad_question_check(user, memories)

    if results:
        return results
    
    # -----------------------------
    # Instant keyword search
    # -----------------------------

    keyword_keys = search_by_keywords(user)

    if keyword_keys:

        scored = []

        for _, key, value, importance in memories:

            if key in keyword_keys:

                score = memory_score(
                    user,
                    key,
                    importance
                )

                scored.append(
                    (
                        score,
                        f"{key}: {value}"
                    )
                )

        scored.sort(reverse=True)

        if scored:

            return [
                memory
                for _, memory in scored
            ]

    # -----------------------------
    # Fast keyword filtering
    # -----------------------------

    words = set(re.findall(r"\w+", user.lower()))

    expanded_words = set(words)

    for word in words:
        key = resolve_key(word)
        if key:
            expanded_words.add(key)
            expanded_words.update(aliases_of(key))

    candidates = []

    for _, key, value, importance in memories:

        aliases = " ".join(aliases_of(key))

        text = f"{key} {aliases} {value}".lower()

        score = 0
        for word in expanded_words:
            if len(word) <= 2:
                continue

            if word in key.lower():
                score += 3

            if word in value.lower():
                score += 1

        # Importance boosts memories you've marked as important
        score += importance * 0.2

        if score > 0:
            candidates.append((score, key, value, importance))

    # If nothing matched, let Qwen see all memories
    if not candidates:

        candidates = [

            (importance, key, value, importance)

            for _, key, value, importance in memories

        ]

    # Keep only the best 10 candidates
    candidates.sort(reverse=True)

    candidates = candidates[:10]

    memory_text = "\n".join(

        f"{key} = {value} (importance {importance})"

        for _, key, value, importance in candidates

    )

    text = normal_chat(

        MODELS["memory"],

        [

            {
                "role": "system",
                "content": load_prompt("search_prompt.txt")
            },

            {
                "role": "user",
                "content":
                    f"Question:\n{user}\n\n"
                    f"Memories:\n{memory_text}"
            }

        ]

    ).strip()

    #print("\nQuestion:", user)
    #print("\nMemory list sent to Search AI:")
    #print(memory_text)
    #print("\nSearch AI returned:")
    #print(text)

    #print("\nMemory AI raw response:", text)

    try:

        keys = json.loads(text)

    except Exception:

        print("\nMemory search failed.")
        print(text)

        return []

    returned = {

        key.strip().lower()

        for key in keys

    }

    results = [

        f"{key}: {value}"

        for _, key, value, _ in candidates

        if key.lower() in returned

    ]

    return results