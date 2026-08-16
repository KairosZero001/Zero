#scores every category and returns the best one, if none are found, returns chat

from models import MODELS


CHAT_WORDS = [
    "hello", "hi", "hey", "thanks", "thank you",
    "good morning", "good night", "how are you"
]

CODING_WORDS = [
    "python", "code", "coding", "program",
    "debug", "bug", "error", "exception",
    "function", "class", "loop",
    "java", "c++", "html", "css",
    "javascript", "sql", "database",
    "api", "github"
]

REASONING_WORDS = [
    "why", "how", "explain", "logic",
    "reason", "algorithm", "math",
    "calculate", "compare",
    "advantages", "disadvantages",
    "prove", "analyze"
]

VISION_WORDS = [
    "image", "picture", "photo",
    "screenshot", "diagram",
    "see", "look at", "identify"
]


def score(text, keywords):

    text = text.lower()

    return sum(
        1
        for word in keywords
        if word in text
    )


def choose_model(user):

    scores = {

        "chat": score(user, CHAT_WORDS),

        "coding": score(user, CODING_WORDS),

        "reasoning": score(user, REASONING_WORDS),

        "vision": score(user, VISION_WORDS)

    }

    best = max(scores, key=scores.get)

    if scores[best] == 0:
        best = "chat"

    return MODELS[best]