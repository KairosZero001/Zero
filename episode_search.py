from episode_database import recent_episodes


def search_episode(question):

    question = question.lower()

    triggers = (

        "yesterday",
        "today",
        "last week",
        "what did i do",
        "what happened",
        "accomplish",
        "completed",
        "worked on",
        "recent"

    )

    if not any(x in question for x in triggers):
        return []

    return recent_episodes()

def format_episodes(rows):

    if not rows:
        return None

    text = []

    for date, summary, importance in rows:

        text.append(
            f"{date} - {summary}"
        )

    return "\n".join(text)