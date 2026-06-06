import os
import json

CHAT_HISTORY_FILE = "data/chat_history.json"


def load_chat_history():

    if not os.path.exists(CHAT_HISTORY_FILE):
        return []

    try:

        with open(
            CHAT_HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return []


def save_chat_history(history):

    os.makedirs("data", exist_ok=True)

    with open(
        CHAT_HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            history,
            f,
            ensure_ascii=False,
            indent=2
        )


def clear_chat_history():

    if os.path.exists(CHAT_HISTORY_FILE):
        os.remove(CHAT_HISTORY_FILE)