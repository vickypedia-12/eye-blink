import requests

def test_health_check():
    response = requests.get("http://localhost:8000/")
    assert response.status_code == 200

def test_login():
    data = {"username": "test", "password": "test"}
    response = requests.post("http://localhost:8000/login", json=data)
    assert response.status_code in (200, 401)