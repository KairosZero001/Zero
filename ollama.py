import json
import requests

from config import OLLAMA_URL, KEEP_ALIVE


def chat(model, messages, stream=True):

    response = requests.post(

        OLLAMA_URL,

        json={
            "model": model,
            "messages": messages,
            "stream": stream,
            "keep_alive": KEEP_ALIVE
        },

        stream=stream

    )

    return response


def stream_chat(model, messages):
    response = chat(model, messages, stream=True)

    reply = ""
    stats = {}

    for line in response.iter_lines():
        if not line:
            continue

        data = json.loads(line)

        if "error" in data:
            raise RuntimeError(data["error"])

        if "message" in data:
            text = data["message"]["content"]
            reply += text

        stats = data

    return reply, stats


def normal_chat(model, messages):
    response = chat(model, messages, stream=False)

    data = response.json()

    if "error" in data:
        print("⚠ Ollama API Error:", data["error"])
        return ""
    
    return data["message"]["content"]