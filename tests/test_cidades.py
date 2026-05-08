import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_cidades_por_estado_valido_200():
    response = client.get("/api/v1/cidades/CE")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["uf"] == "CE"
    assert "cidades" in data
    assert isinstance(data["cidades"], list)
    assert len(data["cidades"]) > 0
    assert "nome" in data["cidades"][0]

def test_cidades_por_estado_sigla_invalida_400():
    response = client.get("/api/v1/cidades/C")
    assert response.status_code == 400
    data = response.json()
    
    assert data["erro"] is True
    assert data["codigo"] == "SIGLA_UF_INVALIDA"
