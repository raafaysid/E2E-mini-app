from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_create_item():
    response = client.post("/items", json = {"name": "Notebook", "price": 10.5})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Notebook"
    assert data["price"] == 10.5
    assert "id" in data

def test_list_items():
    #make sure atleast one item is present
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_item_by_id():
    #creating new item first
    response = client.post("/items", json = {"name": "Pen", "price": 2.0 })
    item_id = response.json()["id"]
    #fetching it back
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Pen"
    assert data["price"] == 2.0

def test_get_item_not_found():
    response = client.get("/items/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"