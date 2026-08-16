import time
import threading

from episode_search import search_episode, format_episodes
from episode_ai import process_episode
from router import choose_model
from session import (
    add_user,
    add_ai,
    get_current_model,
    set_current_model
)

from context import build_context
from ollama import stream_chat
from memory_ai import process_memory
from memory_manager import (
    remember,
    recall,
    forget,
    list_memories
)

def ask_zero(user):

    episodes = search_episode(user)

    if episodes:

        return format_episodes(episodes)

    # --------------------
    # Manual memories
    # --------------------

    for command in (remember, recall, forget, list_memories):
        result = command(user)

        if result:
            return {
                "reply": result,
                "stats": None,
                "elapsed": None,
                "model": None
            }
    
    #--------------------
    # Save conversation
    # --------------------

    add_user(user)

    # --------------------
    # Choose model
    # --------------------

    model = choose_model(user)

    previous = get_current_model()

    if previous != model:

        print(f"\n[Router] Switching to {model}")

        set_current_model(model)

    else:

        print(f"\n[Router] Staying on {model}")

    # --------------------
    # Build prompt
    # --------------------

    messages = build_context(user)

    # --------------------
    # Ask Ollama
    # --------------------

    start = time.perf_counter()

    reply, stats = stream_chat(
        model,
        messages
    )

    elapsed = time.perf_counter() - start

    # --------------------
    # Performance
    # --------------------

    #print_stats(stats, elapsed)

    # --------------------
    # Save reply
    # --------------------

    add_ai(reply)

    # --------------------
    # Learn new memories
    # --------------------

    threading.Thread(
        target=process_memory,
        args=(user,),
        daemon=True
    ).start()

    threading.Thread(
        target=process_episode,
        args=(user,),
        daemon=True
    ).start()

    return {
        "reply": reply,
        "stats": stats,
        "elapsed": elapsed,
        "model": model
    }
