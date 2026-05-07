# API de Agregação de Dados Climáticos e Geográficos

Esta é uma API REST desenvolvida em Python utilizando FastAPI para a agregação de dados climáticos e geográficos. O projeto visa fornecer endpoints estruturados e eficientes para a consulta unificada dessas informações, combinando dados da Brasil API (IBGE/CPTEC) e Open-Meteo.

## Requisitos
- Python 3.9+
- Pip (Gerenciador de pacotes do Python)

## Instalação e Execução

1. Clone o repositório.
2. (Opcional, porém recomendado) Crie um ambiente virtual:
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```
3. Instale as dependências do projeto:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute o servidor de desenvolvimento (que rodará obrigatoriamente na porta 3000):
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 3000 --reload
   ```
5. A documentação interativa (Swagger UI) estará disponível em: [http://localhost:3000/docs](http://localhost:3000/docs)

## Executando os Testes
Para rodar os testes automatizados, utilize o pytest:
```bash
pytest tests/
```
