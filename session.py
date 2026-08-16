#responsible for  current conversations, current active model, automattic history trimming, resetting conversations

from config import MAX_HISTORY
from personality import load_personality


# Conversation history
messages = [
    {
        "role": "system",
        "content": load_personality()
    }
]


# Current active model
current_model = None


def get_messages():
    return messages


def add_user(text):

    messages.append({
        "role": "user",
        "content": text
    })

    trim_history()


def add_ai(text):

    messages.append({
        "role": "assistant",
        "content": text
    })

    trim_history()


def trim_history():

    # Keep:
    # 1 system prompt
    # MAX_HISTORY conversation messages

    while len(messages) > MAX_HISTORY + 1:
        messages.pop(1)


def clear_session():

    global messages

    messages = [
        {
            "role": "system",
            "content": load_personality()
        }
    ]


def get_current_model():
    return current_model


def set_current_model(model):

    global current_model

    current_model = model