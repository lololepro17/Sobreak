import json
import os

HISTORY_PATH = os.path.join(os.path.dirname(__file__), '../database/history.json')

def save_session(session):
    try:
        if os.path.exists(HISTORY_PATH):
            with open(HISTORY_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []
    except Exception:
        data = []
    data.append(session)
    with open(HISTORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_history():
    try:
        with open(HISTORY_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []
