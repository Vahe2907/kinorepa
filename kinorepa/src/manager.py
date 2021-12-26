# adding kinorepa directory
import sys

sys.path.append("../../kinorepa")

import typing

from kinorepa import config
from kinorepa.kinopoisk_api import kinopoisk_client
from kinorepa.models import film, fact
from kinorepa.database import manager as database_manager


client = kinopoisk_client.KinopoiskClient(config.API_KEY)


async def find_film_by_keyword(keyword: str) -> typing.List[int]:
    response = await client.films_search_by_keyword_get(keyword)
    if not response["films"]:
        return None

    return [item["filmId"] for item in response["films"]]


async def find_film_by_id(id: int, db_manager: database_manager.DBManager) -> film.Film:
    kinorepa_film = db_manager.find_film_by_id(id)

    if kinorepa_film is not None:
        return kinorepa_film.markdown_repr

    kinopoisk_film = await client.films_id_get(id)

    kinorepa_film = film.parse_kinopoisk(kinopoisk_film)
    db_manager.insert_film(kinorepa_film)

    return kinorepa_film.markdown_repr


async def find_facts_ids_by_film_id(
    film_id: int, db_manager: database_manager.DBManager
) -> typing.List[int]:
    kinorepa_facts_ids = db_manager.find_facts_ids_by_film_id(film_id)

    if bool(kinorepa_facts_ids):
        return kinorepa_facts_ids

    kinopoisk_facts = await client.films_id_facts_get(film_id)

    kinorepa_facts = [
        fact.parse_kinopoisk(film_id, kinopoisk_fact)
        for kinopoisk_fact in kinopoisk_facts
    ]
    db_manager.insert_facts(kinorepa_facts)

    return db_manager.find_facts_ids_by_film_id(film_id)


async def find_fact_by_id(id: int, db_manager: database_manager.DBManager):
    kinorepa_fact = db_manager.find_fact_by_id(id)

    return kinorepa_fact.markdown_repr
