# database.py
import os
import json
from pathlib import Path

# Simple file-based database for demo
DB_PATH = Path(__file__).parent / "data"
DB_PATH.mkdir(exist_ok=True)

def get_user_by_username(username):
    user_file = DB_PATH / f"user_{username}.json"
    if user_file.exists():
        with open(user_file, 'r') as f:
            return json.load(f)
    return None

def get_user_preferences(user_id):
    pref_file = DB_PATH / f"preferences_{user_id}.json"
    if pref_file.exists():
        with open(pref_file, 'r') as f:
            return json.load(f)
    return {"categories": [], "liked": [], "history": []}

def update_user_preferences(user_id, query, recommendations):
    prefs = get_user_preferences(user_id)
    # Update with new interaction
    prefs['history'].append({
        'query': query,
        'recommendations': recommendations,
        'timestamp': str(datetime.now())
    })
    # Limit history size
    prefs['history'] = prefs['history'][-50:]
    
    pref_file = DB_PATH / f"preferences_{user_id}.json"
    with open(pref_file, 'w') as f:
        json.dump(prefs, f)