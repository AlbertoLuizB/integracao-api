# 🌦️ API de Agregação de Dados Climáticos e Geográficos

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Concluído-success.svg)

> **Projeto Acadêmico:** Atividade avaliativa desenvolvida para a disciplina de **Técnicas de Integração de Sistemas (N703)**.

Esta é uma API RESTful desenvolvida em **Python** utilizando **FastAPI** para a agregação de dados climáticos e geográficos. O objetivo do projeto é fornecer endpoints unificados que processam dinamicamente informações de localidades (buscando apenas pelo nome da cidade) e combinam dados do IBGE com métricas climáticas utilizando a Brasil API e as APIs de Geocoding e Previsão do Open-Meteo.

---

## ✨ Funcionalidades

- **Busca Integrada e Coordenadas Dinâmicas:** Informando apenas o nome da cidade, a API busca dinamicamente suas coordenadas geográficas e consome os dados climáticos, cumprindo a restrição de não usar coordenadas fixas no código.
- **Listagem de Municípios:** Consulta paginada de todas as cidades de um estado específico através de sua sigla (UF).
- **Tratamento Robusto de Erros:** Respostas padronizadas para cidades/estados não encontrados (404), parâmetros inválidos (400) e falha de serviços de terceiros (503).
- **Monitoramento:** Endpoint de *Health Check* para garantir a disponibilidade do serviço interno e da comunicação com APIs externas.

---

## 🚀 Instalação e Execução

### Pré-requisitos
- **Python 3.9** ou superior
- **Git** para clonagem do repositório

### Passo a Passo

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/AlbertoLuizB/integracao-api.git
   cd integracao-api
   ```

2. **Instale as dependências:**
   ```bash
   pip install fastapi uvicorn pydantic pydantic-settings httpx pytest pytest-asyncio
   ```

3. **Inicie o servidor localmente:**
   > A aplicação está configurada para rodar **obrigatoriamente na porta 3000**, conforme os requisitos do projeto.
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 3000 --reload
   ```

4. **Acesse a Documentação Interativa:**
   A API conta com documentação baseada no padrão OpenAPI (Swagger UI).
   - 👉 **Swagger UI:** [http://localhost:3000/docs](http://localhost:3000/docs)

---

## 📡 Endpoints Disponíveis

A API possui as seguintes rotas base (Prefixo: `/api/v1`):

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/health` | Verifica a saúde da API e conectividade com serviços externos. |
| `GET` | `/clima/{nome_cidade}` | Retorna dados geográficos e climáticos da cidade solicitada. |
| `GET` | `/cidades/{sigla_uf}` | Lista municípios de um estado. Suporta o query parameter `?limite=N` (padrão 10). |

> **Postman:** Uma collection completa do Postman com cenários de sucesso e erro está disponível na pasta `docs/postman_collection.json` para facilitar a validação.

---

## 🧪 Testes Automatizados

O projeto utiliza o framework `pytest` para testes de integração, cobrindo cenários de validações e os retornos de erro padronizados. Para executar a suíte de testes na raiz do repositório:

```bash
# No Windows (PowerShell):
$env:PYTHONPATH="."; pytest tests/

# No Linux/Mac:
PYTHONPATH=. pytest tests/
```
