import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check_status():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert "versao" in data
    assert "timestamp" in data
