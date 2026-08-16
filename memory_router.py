MEMORY_KEYWORDS = [
    "what",
    "which",
    "who",
    "where",
    "when",
    "favorite",
    "remember",
    "recall",
    "know",
    "tell me",
    "my",
    "mine",
    "did i",
    "do i",
    "about me"
]


def needs_memory(user):

    text = user.lower()

    return any(word in text for word in MEMORY_KEYWORDS)