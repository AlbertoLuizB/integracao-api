import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_buscar_clima_cidade_valida():
    """
    Testa o requisito obrigatório: Resposta correta para nome de cidade válido.
    """
    response = client.get("/api/v1/clima/Fortaleza")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verifica a estrutura da resposta
    assert data["nome"] == "Fortaleza"
    assert data["estado"] == "CE"
    assert "clima" in data
    assert "temperatura_min" in data["clima"]
    assert "temperatura_max" in data["clima"]
    assert "condicao" in data["clima"]
    assert "consultado_em" in data

def test_buscar_clima_cidade_nao_encontrada():
    """
    Testa o requisito obrigatório: Tratamento de erro para cidade não encontrada.
    """
    response = client.get("/api/v1/clima/CidadeInexistenteXYZ")
    
    assert response.status_code == 404
    data = response.json()
    
    # Verifica o formato exato de erro especificado
    assert data["erro"] is True
    assert data["codigo"] == "CIDADE_NAO_ENCONTRADA"
    assert "mensagem" in data
    assert data["nome_informado"] == "CidadeInexistenteXYZ"

def test_health_check_status():
    """
    Testa se o Health Check está respondendo no formato especificado.
    """
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert "versao" in data
    assert "timestamp" in data

def test_cidades_por_estado_sigla_invalida_400():
    """
    Testa o tratamento de erro para sigla com menos/mais de 2 letras (HTTP 400).
    """
    response = client.get("/api/v1/cidades/C")
    assert response.status_code == 400
    data = response.json()
    
    assert data["erro"] is True
    assert data["codigo"] == "SIGLA_UF_INVALIDA"
