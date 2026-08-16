from relationship_schema import relationship_for


def build_relationship(memory):

    info = relationship_for(memory["key"])

    if info is None:
        return None

    return {
        "subject": info["subject"],
        "relation": info["relation"],
        "object": memory["value"]
    }