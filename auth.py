import json
import os

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({"demo": "demo1"}, f)
        
    with open(USERS_FILE, "r") as f:
        return json.load(f)
    
def authenticate(username, password):
    users = load_users()
    return users.get(username) == password