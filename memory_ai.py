import json

from relationship_builder import build_relationship
from config import MEMORY_RETRIES
from database import save_memory, get_memory, get_confidence
from models import MODELS
from ollama import normal_chat
from prompts import load_prompt
from notifications import add_notification
from memory_schema import (
    MEMORY_SCHEMA,
    is_valid_key, 
    default_importance,
    category_of,
    resolve_key
    )

def validate_memories(memories):

    required = {"category", "key", "value", "importance"}

    valid = []

    for memory in memories:

        if not isinstance(memory, dict):
            print("⚠ Invalid memory:", memory)
            continue

        if not required.issubset(memory.keys()):
            print("⚠ Missing fields:", memory)
            continue

        raw_key = str(memory["key"]).strip().lower().replace(" ", "_")

        key = resolve_key(raw_key)

        if key is None:
            print(f"⚠ Unknown memory key: {raw_key}")
            continue

        memory["key"] = key
        memory["category"] = category_of(key)

        try:
            memory["importance"] = int(
                memory.get(
                    "importance",
                    default_importance(key)
                )
            )
        except Exception:
            memory["importance"] = default_importance(key)

        memory["value"] = str(memory["value"]).strip()

        valid.append(memory)

    return valid

def extract_memories(prompt_text, user_message, is_text=False):

    if is_text:
        system_prompt = prompt_text
    else:
        system_prompt = load_prompt(prompt_text)

    for attempt in range(MEMORY_RETRIES):

        text = normal_chat(
            MODELS["memory"],
            [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        ).strip()

        if text.upper() == "NONE":
            return []

        if text.startswith("```"):
            text = (
                text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

        try:

            memories = json.loads(text)

            if isinstance(memories, dict):
                memories = [memories]

            if isinstance(memories, list):
                return memories

        except Exception:

            print(f"⚠ Retry {attempt+1}/{MEMORY_RETRIES}")

            system_prompt += """

            Your previous response was invalid.

            Return ONLY valid JSON.

            Do not explain anything.

            Do not use markdown.
        
            """
    
    print("⚠ Memory AI returned invalid JSON.")
    print(text)

    return []

def process_memory(user_message):

    # ---------- Pass 1 ----------

    pass1 = validate_memories(
        extract_memories(
            "memory_prompt.txt",
            user_message
        )
    )

    already = [m["key"] for m in pass1]

    # ---------- Pass 2 ----------

    second_prompt = load_prompt("memory_second_pass.txt")

    second_prompt = second_prompt.replace(
        "{MESSAGE}",
        user_message
    )

    second_prompt = second_prompt.replace(
        "{EXTRACTED}",
        json.dumps(pass1, indent=2)
    )

    pass2 = validate_memories(
        extract_memories(
            second_prompt,
            user_message,
            is_text=True
        )
    )

    # ---------- Merge ----------

    memories = pass1.copy()

    existing = {(m["key"], m["value"].lower()) for m in memories}

    for m in pass2:

        pair=(
            m["key"],
            m["value"].lower()
        )
        if pair not in existing:

            memories.append(m)
            existing.add(pair)

    memories.sort(
        key=lambda m: (
            -m["importance"],
            m["key"]
        )
    )    
    
    for memory in memories:

        key = memory["key"]
        value = memory["value"]
        category = memory["category"]
        importance = memory["importance"]

        old = get_memory(key)

        if old is None:
            confidence = 1
            
        elif old == value:
            confidence = get_confidence(key) + 1

        else:
            confidence = 1    

        print("\nMerged memories:")

        for m in memories:
            print(m)

        relationship = build_relationship(memory)

        if relationship:
            print("Relationship:", relationship)

        save_memory(
            category,
            key,
            value,
            importance,
            confidence
        )

        if old is None:
            add_notification(f"🧠 Learned: {key}")

        elif old == value:
            add_notification(f"📈 Confidence Increased: {key}")    
        else:
            add_notification(f"📝 Updated: {key}")