import json
import os
import requests
import psycopg2
from datetime import datetime
USERS_FILE = "users.json"

CACHE_FILE = "blink_cache.json"

def cache_blink_data(blink_data):
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)
    else:
        cache = []
    cache.append(blink_data)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)


def sync_cached_blinks(token, api_url="http://127.0.0.1:8000/api/blink"):
    import os, json
    CACHE_FILE = "blink_cache.json"
    if not os.path.exists(CACHE_FILE):
        return True
    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)
    success = True
    for data in cache:
        result = post_blink_batch(token, data, api_url)
        if result == "expired":
            return "expired"
        if not result:
            success = False
            break
    if success:
        os.remove(CACHE_FILE)
    return success

def cloud_authenticate(username, password, api_url="http://127.0.0.1:8000/api/auth/login"):
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(api_url, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        return None
    
def post_blink_batch(token, data, api_url="http://127.0.0.1:8000/api/blink"):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(api_url, json=data, headers=headers)
        if response.status_code == 401 or response.status_code == 403:
            return "expired"
        print("POST /api/blink status:", response.status_code, response.text)
        return response.status_code == 200
    except Exception as e:
        print("Failed to sync blink data:", e)
        return False
    

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({"demo": "demo1"}, f)
        
    with open(USERS_FILE, "r") as f:
        return json.load(f)
    
def authenticate(username, password):
    users = load_users()
    return users.get(username) == password