import httpx
from src.core.exceptions import APIException

class BrasilAPIService:
    BASE_URL = "https://brasilapi.com.br/api"

    async def get_cidades_por_estado(self, uf: str) -> list:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.BASE_URL}/ibge/municipios/v1/{uf}")
                if response.status_code == 404:
                    raise APIException(
                        status_code=404,
                        code="UF_NAO_ENCONTRADA",
                        message="Estado com a sigla informada não foi encontrado",
                        extra_data={"sigla_uf_informada": uf}
                    )
                response.raise_for_status()
                return response.json()
            except httpx.RequestError:
                raise APIException(
                    status_code=503,
                    code="SERVICO_EXTERNO_INDISPONIVEL",
                    message="Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
                    extra_data={"servico": "IBGE/BrasilAPI"}
                )

    async def get_cidade_cptec(self, nome_cidade: str) -> dict:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.BASE_URL}/cptec/v1/cidade/{nome_cidade}")
                if response.status_code == 404:
                    raise APIException(
                        status_code=404,
                        code="CIDADE_NAO_ENCONTRADA",
                        message="Nenhuma cidade encontrada com o nome informado",
                        extra_data={"nome_informado": nome_cidade}
                    )
                response.raise_for_status()
                cidades = response.json()
                if not cidades:
                    raise APIException(
                        status_code=404,
                        code="CIDADE_NAO_ENCONTRADA",
                        message="Nenhuma cidade encontrada com o nome informado",
                        extra_data={"nome_informado": nome_cidade}
                    )
                # Se retornar uma lista, retorna a primeira cidade
                return cidades[0] if isinstance(cidades, list) else cidades
            except httpx.RequestError:
                raise APIException(
                    status_code=503,
                    code="SERVICO_EXTERNO_INDISPONIVEL",
                    message="Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
                    extra_data={"servico": "CPTEC/BrasilAPI"}
                )

    async def get_clima_cptec(self, city_code: int) -> dict:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.BASE_URL}/cptec/v1/clima/previsao/{city_code}")
                if response.status_code == 404:
                    raise APIException(
                        status_code=404,
                        code="CIDADE_NAO_ENCONTRADA",
                        message="Nenhuma cidade encontrada para buscar a previsão",
                        extra_data={"city_code_informado": city_code}
                    )
                response.raise_for_status()
                return response.json()
            except httpx.RequestError:
                raise APIException(
                    status_code=503,
                    code="SERVICO_EXTERNO_INDISPONIVEL",
                    message="Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
                    extra_data={"servico": "CPTEC/BrasilAPI"}
                )

brasil_api_service = BrasilAPIService()
