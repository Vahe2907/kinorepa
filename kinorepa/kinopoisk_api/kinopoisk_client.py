import aiohttp

from pprint import pprint


class KinopoiskClient:
    """
    Клиент для работы с KinopoiskApiUnofficial (https://kinopoiskapiunofficial.tech/)

    Поля:
      - api_key: ключ из профиля KinopoiskApiUnofficial (https://kinopoiskapiunofficial.tech/profile)
    """

    def __init__(self, api_key: str):
        self._api_key = api_key

        self._endpoints = {
            "films/{id}": {
                "get": "https://kinopoiskapiunofficial.tech/api/v2.2/films/{}"
            }
        }

    async def _request(
        self, method: str, endpoint: str, headers: dict, query: dict, body: dict
    ) -> dict:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method=method,
                    url=endpoint,
                    headers=headers,
                    params=query,
                    json=body,
                ) as response:
                    print(response.status)
                    if response.status == 200:
                        response_json = await response.json()
                        return response_json

                    response_json = await response.json()
                    print(response_json)
                    return None
            except aiohttp.ClientConnectionError as err:
                return None

    async def films_id_get(self, id: int):
        endpoint = self._endpoints["films/{id}"]["get"].format(id)
        headers = {
            "X-API-KEY": self._api_key,
            "Content-Type": "application/json",
        }

        response = await self._request("GET", endpoint, headers, {}, {})

        pprint(response)

        return response
