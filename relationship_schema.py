RELATIONSHIPS = {

    "pet_name": {
        "subject": "user",
        "relation": "has_pet"
    },

    "favorite_game": {
        "subject": "user",
        "relation": "likes"
    },

    "favorite_movie": {
        "subject": "user",
        "relation": "likes"
    },

    "favorite_food": {
        "subject": "user",
        "relation": "likes"
    },

    "favorite_color": {
        "subject": "user",
        "relation": "likes"
    },

    "graphics": {
        "subject": "laptop",
        "relation": "has_gpu"
    },

    "cpu": {
        "subject": "laptop",
        "relation": "has_cpu"
    },

    "project": {
        "subject": "user",
        "relation": "building"
    },

    "dream": {
        "subject": "user",
        "relation": "dreams_of"
    }
}

def relationship_for(key):
    return RELATIONSHIPS.get(key)