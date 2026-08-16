from memory_schema import resolve_key

broad_questions = (
    "everything",
    "all",
    "about me",
    "know about me",
    "remember about me",
)

def broad_question_check(user, memories):

    if any(x in user.lower() for x in broad_questions):
        return [
            f"{key}: {value}"
            for _, key, value, _ in memories
        ]
    
    return []

def search_by_keywords(question):

    found = set()

    text = question.lower()

    # Whole sentence
    key = resolve_key(text)

    if key:
        found.add(key)

    # Individual words
    words = text.split()

    for word in words:

        key = resolve_key(word)

        if key and key not in found:
            found.add(key)

    # Two-word phrases
    for i in range(len(words) - 1):

        phrase = words[i] + " " + words[i + 1]

        key = resolve_key(phrase)

        if key and key not in found:
            found.add(key)

    # Three-word phrases
    for i in range(len(words) - 2):

        phrase = " ".join(words[i:i+3])

        key = resolve_key(phrase)

        if key and key not in found:
            found.add(key)        

    return list(found)

from memory_schema import aliases_of


def memory_score(question, key, importance):

    score = importance

    text = question.lower()

    if key in text:
        score += 5

    for alias in aliases_of(key):

        if alias in text:
            score += 3

    return score