import json

from datetime import date

from models import MODELS
from ollama import normal_chat
from prompts import load_prompt
from episode_database import save_episode, episode_exists


def process_episode(user_message):

    text = normal_chat(

        MODELS["memory"],

        [

            {
                "role": "system",
                "content": load_prompt("episode_prompt.txt")
            },

            {
                "role": "user",
                "content": user_message
            }

        ]

    ).strip()

    if text.upper() == "NONE":
        return

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    try:
        episode = json.loads(text)

    except Exception:

        print("⚠ Invalid JSON returned by Episode AI:")
        print(text)
        return
    
    if "summary" not in episode:

        print("⚠ Episode missing summary.")
        return

    summary = episode["summary"].strip()

    try:
        importance = int(
            episode.get("importance", 5)
        )

    except Exception:
        importance = 5

    today = date.today().isoformat()   

    prompt = load_prompt("episode_prompt.txt")

    prompt = prompt.replace(
        "{TODAY}",
        today
    ) 

    if episode_exists(summary):
        return

    save_episode(

        today,

        summary,

        importance

    )

    print(f"📖 Episode saved: {summary}")