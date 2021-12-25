# adding kinorepa directory
import sys

import kinorepa

sys.path.append("../../kinorepa")

import asyncio

from kinorepa import config
from kinorepa.kinopoisk_api import kinopoisk_client
from kinorepa.models import film

client = kinopoisk_client.KinopoiskClient(config.API_KEY)


async def find_by_keyword(keyword: str) -> film.Film:
    response = await client.films_search_by_keyword_get(keyword)
    if not response["films"]:
        return None

    first_film = response["films"][0]

    kinopoisk_film = await client.films_id_get(first_film["filmId"])
    kinorepa_film = film.parse(kinopoisk_film)

    return kinorepa_film.markdown_repr
