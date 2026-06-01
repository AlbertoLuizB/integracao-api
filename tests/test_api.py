import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_buscar_clima_cidade_valida():
    response = client.get("/api/v1/clima/Fortaleza")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["nome"] == "Fortaleza"
    assert data["estado"] == "CE"
    assert "clima" in data
    assert "temperatura_min" in data["clima"]
    assert "temperatura_max" in data["clima"]
    assert "condicao" in data["clima"]
    assert "consultado_em" in data

def test_buscar_clima_cidade_nao_encontrada():
    response = client.get("/api/v1/clima/CidadeInexistenteXYZ")
    
    assert response.status_code == 404
    data = response.json()
    
    assert data["erro"] is True
    assert data["codigo"] == "CIDADE_NAO_ENCONTRADA"
    assert "mensagem" in data
    assert data["nome_informado"] == "CidadeInexistenteXYZ"
