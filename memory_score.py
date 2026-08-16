from memory_schema import aliases_of

def memory_score(question, key, importance):
    question = question.lower()

    score = 0

    # Direct key match
    if key.lower() in question:
        score += 5

    # Alias match
    for alias in aliases_of(key):
        if alias.lower() in question:
            score += 4

    # Importance bonus
    score += importance * 0.2

    return score