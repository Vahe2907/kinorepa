# adding kinorepa directory
import sys

sys.path.append("../../kinorepa")

import re

from kinorepa.utils import utils


class Fact:
    """
    Интересный факт о фильме

    Поля:
      - film_id: int (идентификатор фильма)

      - text: str (сам факт)
      - is_spoiler: int (является ли этот факт спойлером к фильму)
    """

    def __init__(self, film_id: int, text: str, is_spoiler: int):
        self._film_id = film_id

        self._text = text
        self._is_spoiler = is_spoiler

    @property
    def markdown_repr(self):
        result = []

        result.append(f"*Спойлер*: {'Да' if self._is_spoiler else 'Нет'}")
        result.append(f"*Факт*: {self._text}")

        return "\n\n".join(result)

    @property
    def to_list(self):
        return [self._film_id, self._text, self._is_spoiler]


def parse_kinopoisk(film_id: int, kinopoisk_fact: dict) -> Fact:
    text = utils.parse_text(kinopoisk_fact["text"])
    is_spoiler = int(kinopoisk_fact["spoiler"])

    return Fact(film_id, text, is_spoiler)


def parse_db(args) -> Fact:
    return Fact(*args)
