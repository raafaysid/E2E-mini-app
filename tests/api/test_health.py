from fastapi.testclient import TestClient
from backend.app.main import app

# Testclient to call the fastapi app in memory
client = TestClient(app)

def test_health_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
