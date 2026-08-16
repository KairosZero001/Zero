# ===========
# Ollama
# ===========

OLLAMA_URL = "http://localhost:11434/api/chat"

KEEP_ALIVE = "1h"


# ===========
# Conversation
# ===========

MAX_HISTORY = 30


# ===========
# Memory
# ===========

MEMORY_DB = "memories/zero.db"


# ===========
# Models
# ===========

CHAT_MODEL = "mistral:latest"

CODING_MODEL = "qwen2.5:7b"

REASONING_MODEL = "qwen3:8b"

VISION_MODEL = "qwen2.5vl:7b"

MEMORY_MODEL = "qwen2.5:7b"


# ===========
# Generation
# ===========

TEMPERATURE = 0.7

TOP_P = 0.9

MEMORY_RETRIES = 2