import os, requests
from jsonschema import validate

BACKEND = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

def test_health_contract():
    schema = {
        "type": "object",
        "properties": {"status": {"type": "string"}},
        "required": ["status"],
        "additionalProperties": True,
    }
    r = requests.get(f"{BACKEND}/health", timeout=3); r.raise_for_status()
    validate(instance=r.json(), schema=schema)

def test_items_list_contract():
    item_schema = {
        "type": "object",
        "properties": {
            "id": {"type": ["integer", "string"]},
            "name": {"type": "string"},
            "price": {"type": ["number", "string"]},
        },
        "required": ["name", "price"],
        "additionalProperties": True,
    }
    list_schema = {"type": "array", "items": item_schema}

    r = requests.get(f"{BACKEND}/items", timeout=5); r.raise_for_status()
    validate(instance=r.json(), schema=list_schema)
