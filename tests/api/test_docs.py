import os, requests

BACKEND = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

def test_fastapi_docs_http_200():
    r = requests.get(f"{BACKEND}/docs", timeout=5)
    assert r.status_code == 200

def test_openapi_json_contract_present():
    r = requests.get(f"{BACKEND}/openapi.json", timeout=5)
    r.raise_for_status()
    data = r.json()
    assert "paths" in data and isinstance(data["paths"], dict)
