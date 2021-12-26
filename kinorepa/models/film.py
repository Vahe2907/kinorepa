# adding kinorepa directory
import sys

sys.path.append("../../kinorepa")

import datetime

from kinorepa.utils import utils


class Film:
    """
    Фильм

    Поля:
      - id: int (уникальный идентификатор)

      - filmcrew_id: int (идентификатор съёмочной команды)
      - genres: str (жанр фильма)

      - kinopoisk_id: int (идентификатор фильма в Кинопоиске)
      - imdb_id: int (идентификатор фильма в Imdb)

      - name: str (название фильма)
      - description: str (описание к фильму)

      - budget: int (бюджет фильма)
      - fees: int (сборы фильма)

      - duration: int (длительность фильма)

      - rating_kinopoisk: float (рейтинг фильма в Кинопоиске)
      - rating_imdb: float (рейтинг фильма в Imdb)
      - rating_kinorepa: float (рейтинг фильма в Kinorepa)

      - release_year: int (год выпуска фильма)
      - updated_at: datetime (дата последнего обновления данных о фильме)
      - published_at: datetime (дата добавления фильма в Kinorepa)
    """

    def __init__(
        self,
        id: int,
        filmcrew_id: int,
        genres: str,
        kinopoisk_id: int,
        imdb_id: int,
        name_ru: str,
        name_orig: str,
        description: str,
        budget: int,
        fees: int,
        duration: int,
        rating_kinopoisk: float,
        rating_imdb: float,
        rating_kinorepa: float,
        release_year: int,
        updated_at: datetime.datetime,
        published_at: datetime.datetime,
        poster_url: str,
    ):
        self._id = id

        self._filmcrew_id = filmcrew_id
        self._genres = genres

        self._kinopoisk_id = kinopoisk_id
        self._imdb_id = imdb_id

        self._name_ru = name_ru
        self._name_orig = name_orig
        self._description = description

        self._budget = budget
        self._fees = fees

        self._duration = duration

        self._rating_kinopoisk = rating_kinopoisk
        self._rating_imdb = rating_imdb
        self._rating_kinorepa = rating_kinorepa

        self._release_year = release_year
        self._updated_at = updated_at
        self._published_at = published_at

        self._poster_url = poster_url

    @property
    def markdown_repr(self):
        result = []

        if self._name_ru is not None:
            result.append(f"*Название*: {self._name_ru}")

            if self._name_orig is not None:
                result[-1] += f" ({self._name_orig})"

        if self._name_ru is None and self._name_orig is not None:
            result.append(f"*Название*: {self._name_orig}")

        if self._description is not None:
            result.append(f"*Описание*: {self._description}")

        if self._duration is not None:
            result.append(f"*Длительность*: {self._duration} минут")

        if self._genres is not None:
            result.append(f"*Жанры*: {self._genres}")

        if self._rating_kinopoisk is not None:
            ratings = []

            ratings.append(f"*Рейтинги:*")
            ratings.append(f"  - _Кинопоиск_: {self._rating_kinopoisk}")

            if self._rating_imdb is not None:
                ratings.append(f"  - _Imdb_: {self._rating_imdb}")

            if self._rating_kinorepa is not None:
                ratings.append(f"  - _Кинорепа:_: {self._rating_kinorepa}")

            result.append("\n".join(ratings))

        if self._release_year is not None:
            result.append(f"*Год*: {self._release_year}")

        if self._poster_url is not None:
            result.append(f"[Постер]({self._poster_url})")

        return "\n\n".join(result)

    @property
    def to_list(self):
        return [
            self._id,
            self._filmcrew_id,
            self._genres,
            self._kinopoisk_id,
            self._imdb_id,
            self._name_ru,
            self._name_orig,
            self._description,
            self._budget,
            self._fees,
            self._duration,
            self._rating_kinopoisk,
            self._rating_kinorepa,
            self._rating_imdb,
            self._release_year,
            self._updated_at,
            self._published_at,
            self._poster_url,
        ]


def parse_kinopoisk(kinopoisk_film: dict):
    id = kinopoisk_film["kinopoiskId"]

    filmcrew_id = 0  # TODO
    genres = ", ".join([genre["genre"] for genre in kinopoisk_film["genres"]])

    kinopoisk_id = kinopoisk_film["kinopoiskId"]
    imdb_id = kinopoisk_film["imdbId"]

    name_ru = kinopoisk_film["nameRu"]
    name_orig = kinopoisk_film["nameOriginal"]
    description = utils.parse_text(kinopoisk_film["description"])

    budget = 100
    fees = 100

    duration = kinopoisk_film["filmLength"]

    rating_kinopoisk = kinopoisk_film["ratingKinopoisk"]
    rating_imdb = kinopoisk_film["ratingImdb"]
    rating_kinorepa = None

    release_year = kinopoisk_film["year"]
    updated_at = datetime.datetime.now()
    published_at = datetime.datetime.now()

    poster_url = kinopoisk_film["posterUrl"]

    return Film(
        id,
        filmcrew_id,
        genres,
        kinopoisk_id,
        imdb_id,
        name_ru,
        name_orig,
        description,
        budget,
        fees,
        duration,
        rating_kinopoisk,
        rating_imdb,
        rating_kinorepa,
        release_year,
        updated_at,
        published_at,
        poster_url,
    )


def parse_db(args):
    return Film(*args)
