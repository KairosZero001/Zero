MEMORY_SCHEMA = {

    "favorite_name": {
        "category": "preference",
        "description": "The user's preferred name.",
        "importance": 8,
        "aliases": ["name", "preferred name"]
    },

    "favorite_color": {
        "category": "preference",
        "description": "The user's favorite color.",
        "importance": 8,
        "aliases": ["color", "favourite color"]
    },

    "favorite_food": {
        "category": "preference",
        "description": "The user's favorite food.",
        "importance": 8,
        "aliases": ["food", "meal", "cuisine", "favorite meal"]
    },

    "favorite_movie": {
        "category": "preference",
        "description": "The user's favorite movie.",
        "importance": 8,
        "aliases": ["movie", "film"]
    },

    "favorite_game": {
        "category": "preference",
        "description": "The user's favorite game.",
        "importance": 8,
        "aliases": ["game", "video game"]
    },

    "favorite_book": {
        "category": "preference",
        "description": "The user's favorite book.",
        "importance": 7,
        "aliases": ["book", "novel"]
    },

    "favorite_music": {
        "category": "preference",
        "description": "The user's favorite music.",
        "importance": 7,
        "aliases": ["music", "song", "artist", "band"]
    },

    "pet_name": {
        "category": "personal",
        "description": "Name of the user's pet.",
        "importance": 9,
        "aliases": ["dog", "cat", "pet", "puppy", "kitten"]
    },

    "dream": {
        "category": "goal",
        "description": "The user's dream or long-term goal.",
        "importance": 10,
        "aliases": ["dream", "goal", "ambition", "life goal"]
    },

    "project": {
        "category": "project",
        "description": "Current long-term project.",
        "importance": 9,
        "aliases": ["project", "app", "game", "software", "assistant"]
    },

    "programming_language": {
        "category": "education",
        "description": "Programming language the user is learning or mainly uses.",
        "importance": 8,
        "aliases": ["python", "java", "c++", "javascript", "coding language"]
    },

    "editor": {
        "category": "tool",
        "description": "Preferred code editor.",
        "importance": 6,
        "aliases": ["editor", "vscode", "vs code", "pycharm"]
    },

    "graphics": {
        "category": "hardware",
        "description": "GPU or graphics card.",
        "importance": 8,
        "aliases": ["gpu", "graphics", "graphics card", "video card", "rtx", "gtx"]
    },

    "cpu": {
        "category": "hardware",
        "description": "CPU or processor.",
        "importance": 8,
        "aliases": ["cpu", "processor", "ryzen", "intel"]
    },

    "course": {
        "category": "education",
        "description": "Course or major.",
        "importance": 8,
        "aliases": ["course", "major", "degree", "subject"]
    },

    "university": {
        "category": "education",
        "description": "University or college.",
        "importance": 8,
        "aliases": ["university", "college", "campus"]
    },

    "hobby": {
        "category": "personal",
        "description": "Long-term hobby.",
        "importance": 7,
        "aliases": ["hobby", "interest", "pastime"]
    },

    "location": {
        "category": "personal",
        "description": "General location.",
        "importance": 6,
        "aliases": ["city", "country", "state", "location", "place"]
    }
}

def is_valid_key(key):
    return key in MEMORY_SCHEMA


def default_importance(key):
    return MEMORY_SCHEMA[key].get("importance", 5)


def category_of(key):
    return MEMORY_SCHEMA[key]["category"]


def aliases_of(key):
    return MEMORY_SCHEMA[key].get("aliases", [])

def resolve_key(text):

    text = text.lower().strip()

    # Exact key
    if text in MEMORY_SCHEMA:
        return text

    # Exact alias
    for key, info in MEMORY_SCHEMA.items():

        for alias in info.get("aliases", []):

            if text == alias:
                return key

    # Partial match
    for key, info in MEMORY_SCHEMA.items():

        for alias in info.get("aliases", []):

            if alias in text:
                return key

    return None