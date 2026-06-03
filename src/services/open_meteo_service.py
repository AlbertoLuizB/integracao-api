import httpx
from src.core.exceptions import APIException

class OpenMeteoService:
    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

    WMO_CODES = {
        0: "Céu limpo",
        1: "Principalmente claro",
        2: "Parcialmente nublado",
        3: "Encoberto",
        45: "Nevoeiro",
        48: "Nevoeiro depositando geada",
        51: "Garoa leve",
        53: "Garoa moderada",
        55: "Garoa densa",
        56: "Garoa congelante leve",
        57: "Garoa congelante densa",
        61: "Chuva leve",
        63: "Chuva moderada",
        65: "Chuva forte",
        66: "Chuva congelante leve",
        67: "Chuva congelante forte",
        71: "Queda de neve leve",
        73: "Queda de neve moderada",
        75: "Queda de neve forte",
        77: "Grãos de neve",
        80: "Pancadas de chuva leves",
        81: "Pancadas de chuva moderadas",
        82: "Pancadas de chuva violentas",
        85: "Pancadas de neve leves",
        86: "Pancadas de neve fortes",
        95: "Trovoada",
        96: "Trovoada com granizo leve",
        99: "Trovoada com granizo forte"
    }

    ESTADOS_BR = {
        "Acre": "AC", "Alagoas": "AL", "Amapá": "AP", "Amazonas": "AM",
        "Bahia": "BA", "Ceará": "CE", "Distrito Federal": "DF", "Espírito Santo": "ES",
        "Goiás": "GO", "Maranhão": "MA", "Mato Grosso": "MT", "Mato Grosso do Sul": "MS",
        "Minas Gerais": "MG", "Pará": "PA", "Paraíba": "PB", "Paraná": "PR",
        "Pernambuco": "PE", "Piauí": "PI", "Rio de Janeiro": "RJ", "Rio Grande do Norte": "RN",
        "Rio Grande do Sul": "RS", "Rondônia": "RO", "Roraima": "RR", "Santa Catarina": "SC",
        "São Paulo": "SP", "Sergipe": "SE", "Tocantins": "TO"
    }

    async def get_coordenadas(self, nome_cidade: str) -> dict:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.GEOCODING_URL,
                    params={
                        "name": nome_cidade,
                        "count": 1,
                        "language": "pt"
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                results = data.get("results", [])
                if not results:
                    raise APIException(
                        status_code=404,
                        code="CIDADE_NAO_ENCONTRADA",
                        message="Nenhuma cidade encontrada com o nome informado",
                        extra_data={"nome_informado": nome_cidade}
                    )
                
                cidade = results[0]
                estado_nome = cidade.get("admin1", "Não informado")
                estado_sigla = self.ESTADOS_BR.get(estado_nome, estado_nome)
                
                return {
                    "nome": cidade.get("name"),
                    "estado": estado_sigla,
                    "latitude": cidade.get("latitude"),
                    "longitude": cidade.get("longitude")
                }
            except httpx.RequestError:
                raise APIException(
                    status_code=503,
                    code="SERVICO_EXTERNO_INDISPONIVEL",
                    message="Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
                    extra_data={"servico": "Open-Meteo Geocoding"}
                )

    async def get_clima(self, latitude: float, longitude: float) -> dict:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.WEATHER_URL,
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        "daily": "weathercode,temperature_2m_max,temperature_2m_min",
                        "timezone": "auto"
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                daily = data.get("daily", {})
                
                if not daily.get("time"):
                    raise APIException(
                        status_code=404,
                        code="CLIMA_NAO_ENCONTRADO",
                        message="Não foi possível encontrar a previsão do tempo para esta localidade.",
                    )
                
                temp_min = daily.get("temperature_2m_min", [None])[0]
                temp_max = daily.get("temperature_2m_max", [None])[0]
                weathercode = daily.get("weathercode", [None])[0]
                
                if temp_min is not None and temp_max is not None and temp_min > temp_max:
                    temp_min, temp_max = temp_max, temp_min

                condicao = self.WMO_CODES.get(weathercode, "Condição não especificada")
                
                if temp_min is not None:
                    temp_min = round(temp_min)
                if temp_max is not None:
                    temp_max = round(temp_max)

                return {
                    "temperatura_min": temp_min,
                    "temperatura_max": temp_max,
                    "condicao": condicao
                }
            except httpx.RequestError:
                raise APIException(
                    status_code=503,
                    code="SERVICO_EXTERNO_INDISPONIVEL",
                    message="Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
                    extra_data={"servico": "Open-Meteo Weather"}
                )

open_meteo_service = OpenMeteoService()
