from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_login_success():
    response = client.post("/login", json ={"username":"admin","password":"fakepass"})
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_failure():
    response = client.post("/login", json= {"username":"wrong", "password": "bad"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Credentials"