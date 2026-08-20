"""
Integration tests for FastAPI endpoints.
"""
from fastapi.testclient import TestClient
from app.models.database import init_db
from app.main import app

init_db()
client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app_name" in data

def test_diagnostics_endpoint():
    response = client.get("/api/diagnostics")
    assert response.status_code == 200
    data = response.json()
    assert "checks" in data

def test_get_brightness_endpoint():
    response = client.get("/api/brightness")
    assert response.status_code == 200
    data = response.json()
    assert "brightness" in data

def test_set_brightness_endpoint():
    response = client.post("/api/brightness", json={"brightness": 65.0})
    assert response.status_code == 200
    data = response.json()
    assert data["brightness"] == 65.0

def test_get_settings_endpoint():
    response = client.get("/api/settings")
    assert response.status_code == 200
    data = response.json()
    assert "smoothing_factor" in data
    assert "min_brightness" in data

def test_statistics_endpoint():
    response = client.get("/api/statistics")
    assert response.status_code == 200
    data = response.json()
    assert "average_brightness" in data
