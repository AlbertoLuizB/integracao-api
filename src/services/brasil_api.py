import httpx
from src.core.exceptions import APIException

class BrasilAPIService:
    BASE_URL = "https://brasilapi.com.br/api"

    async def check_health(self) -> bool:
        """Faz um ping rápido na API para verificar se está online."""
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                response = await client.get(f"{self.BASE_URL}/ibge/uf/v1")
                return response.status_code == 200
        except Exception:
            return False

    async def get_cidades_por_estado(self, uf: str) -> list:
        """Busca todas as cidades de um estado usando a API do IBGE."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.BASE_URL}/ibge/municipios/v1/{uf.upper()}?providers=dados-abertos-br,gov,wikipedia")
        except httpx.RequestError:
            raise APIException(
                status_code=503,
                code="SERVICO_EXTERNO_INDISPONIVEL",
                message="Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
                extra_data={"servico": "IBGE"}
            )
            
        if response.status_code == 404:
            raise APIException(
                status_code=404,
                code="UF_NAO_ENCONTRADA",
                message="Estado com a sigla informada não foi encontrado",
                extra_data={"sigla_uf_informada": uf}
            )
            
        if response.status_code != 200:
            raise APIException(
                status_code=503,
                code="SERVICO_EXTERNO_INDISPONIVEL",
                message="Falha de comunicação com o serviço externo.",
                extra_data={"servico": "IBGE"}
            )
            
        return response.json()

    async def buscar_cidade_por_nome(self, nome: str) -> list:
        """Busca o código de uma cidade pelo nome usando o CPTEC."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.BASE_URL}/cptec/v1/cidade/{nome}")
        except httpx.RequestError:
            raise APIException(
                status_code=503,
                code="SERVICO_EXTERNO_INDISPONIVEL",
                message="Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
                extra_data={"servico": "CPTEC"}
            )
            
        if response.status_code == 404:
            raise APIException(
                status_code=404,
                code="CIDADE_NAO_ENCONTRADA",
                message="Nenhuma cidade encontrada com o nome informado",
                extra_data={"nome_informado": nome}
            )
            
        if response.status_code != 200:
            raise APIException(
                status_code=503,
                code="SERVICO_EXTERNO_INDISPONIVEL",
                message="Falha de comunicação com o serviço externo.",
                extra_data={"servico": "CPTEC"}
            )
            
        data = response.json()
        if not data:
            raise APIException(
                status_code=404,
                code="CIDADE_NAO_ENCONTRADA",
                message="Nenhuma cidade encontrada com o nome informado",
                extra_data={"nome_informado": nome}
            )
            
        return data

    async def buscar_clima_por_codigo(self, codigo: int) -> dict:
        """Busca o clima de uma cidade usando o código CPTEC fornecido."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.BASE_URL}/cptec/v1/clima/previsao/{codigo}")
        except httpx.RequestError:
            raise APIException(
                status_code=503,
                code="SERVICO_EXTERNO_INDISPONIVEL",
                message="Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
                extra_data={"servico": "CPTEC"}
            )
            
        if response.status_code != 200:
            raise APIException(
                status_code=503,
                code="SERVICO_EXTERNO_INDISPONIVEL",
                message="Falha de comunicação com o serviço externo.",
                extra_data={"servico": "CPTEC"}
            )
            
        return response.json()

brasil_api_service = BrasilAPIService()
