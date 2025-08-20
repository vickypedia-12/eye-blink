import requests

BASE_URL = "https://blink-backend.vickypedia.tech"

def test_health_check():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200

def test_login():
    data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", data=data)
    # Accept 200 (success) or 400/401 (invalid creds)
    assert response.status_code in (200, 400, 401)