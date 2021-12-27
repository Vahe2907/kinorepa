# adding kinorepa directory
from sqlite3.dbapi2 import Date
import sys

sys.path.append("../../kinorepa")

import datetime

from kinorepa.utils import utils
from kinorepa.kinopoisk_api import kinopoisk_client


class Expenses:
    """
    Затраты на производство фильма

    Поля:
      - budget: float (бюджет фильма, в долларах)
      - marketing: float (сколько было потрачено на маркетинг, в долларах)
      - fees_ru: float (сборы в России, в долларах)
      - fees_usa: float (сборы в США, в долларах)
      - fees_world: float (сборы в мире, в долларах)
    """

    def __init__(
        self,
        budget=None,
        marketing=None,
        fees_ru=None,
        fees_usa=None,
        fees_world=None,
    ):
        self.budget = budget
        self.marketing = marketing

        self.fees_ru = fees_ru
        self.fees_usa = fees_usa
        self.fees_world = fees_world


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

      - expenses: Expenses (затраты)

      - duration: int (длительность фильма)

      - rating_kinopoisk: float (рейтинг фильма в Кинопоиске)
      - rating_imdb: float (рейтинг фильма в Imdb)
      - rating_kinorepa: float (рейтинг фильма в Kinorepa)

      - release_year: int (год выпуска фильма)
      - premiere_ru: datetime (премьера в России)
      - premiere_world: datetime (мировая премьера)

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
        expenses: Expenses,
        duration: int,
        rating_kinopoisk: float,
        rating_imdb: float,
        rating_kinorepa: float,
        release_year: int,
        premiere_ru: datetime.datetime,
        premiere_world: datetime.datetime,
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

        self._expenses = expenses

        self._duration = duration

        self._rating_kinopoisk = rating_kinopoisk
        self._rating_imdb = rating_imdb
        self._rating_kinorepa = rating_kinorepa

        self._release_year = release_year

        self._premiere_ru = self._parse_datetime(premiere_ru)
        self._premiere_world = self._parse_datetime(premiere_world)

        self._updated_at = updated_at
        self._published_at = published_at

        self._poster_url = poster_url

    def _parse_datetime(self, date):
        if date is None:
            return None

        if len(date.split()) == 1:
            return datetime.datetime.strptime(date, "%Y-%m-%d")
        else:
            return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

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
            result.append(f"*Длительность*: {self._duration} минут 🕗")

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

        if self._expenses is not None and (
            self._expenses.budget is not None or self._expenses.marketing is not None
        ):
            expenses = []

            if (
                self._expenses.budget is not None
                or self._expenses.marketing is not None
            ):
                expenses.append("*Затраты*:")

            if self._expenses.budget is not None:
                expenses.append("  - _Бюджет_: $ {:,d}".format(self._expenses.budget))
            if self._expenses.marketing is not None:
                expenses.append(
                    "  - _Маркетинг_: $ {:,d}".format(self._expenses.marketing)
                )

            if (
                self._expenses.fees_ru is not None
                or self._expenses.fees_usa is not None
                or self._expenses.fees_world
            ):
                expenses.append("*Сборы* 💰:")

            if self._expenses.fees_ru is not None:
                expenses.append("  - 🇷🇺: $ {:,d}".format(self._expenses.fees_ru))
            if self._expenses.fees_usa is not None:
                expenses.append("  - 🇺🇸: $ {:,d}".format(self._expenses.fees_usa))
            if self._expenses.fees_world is not None:
                expenses.append("  - 🌍: $ {:,d}".format(self._expenses.fees_world))

            result.append("\n".join(expenses))

        if self._release_year is not None:
            result.append(f"*Год*: {self._release_year}")

        if self._premiere_ru is not None or self._premiere_world is not None:
            premieres = []

            if self._premiere_ru is not None:
                premieres.append(
                    f"*Премьера в России*: {utils.date_to_str(self._premiere_ru)}"
                )
            if self._premiere_world is not None:
                premieres.append(
                    f"*Мировая премьера*: {utils.date_to_str(self._premiere_world)}"
                )

            result.append("\n".join(premieres))

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
            self._expenses.budget,
            self._expenses.marketing,
            self._expenses.fees_ru,
            self._expenses.fees_usa,
            self._expenses.fees_world,
            self._duration,
            self._rating_kinopoisk,
            self._rating_kinorepa,
            self._rating_imdb,
            self._release_year,
            self._premiere_ru,
            self._premiere_world,
            self._updated_at,
            self._published_at,
            self._poster_url,
        ]


async def get_budget_and_fees(
    id: int, client: kinopoisk_client.KinopoiskClient
) -> Expenses:
    expenses = {}

    box_office = await client.films_id_box_office_get(id)

    for item in box_office:
        if item["name"] != "US Dollar":
            continue

        if item["type"] == "BUDGET":
            expenses["budget"] = item["amount"]
        elif item["type"] == "MARKETING":
            expenses["marketing"] = item["amount"]
        elif item["type"] == "RUS":
            expenses["fees_ru"] = item["amount"]
        elif item["type"] == "USA":
            expenses["fees_usa"] = item["amount"]
        elif item["type"] == "WORLD":
            expenses["fees_world"] = item["amount"]

    return Expenses(**expenses)


async def get_premieres(id: int, client: kinopoisk_client.KinopoiskClient):
    premieres = {}

    distributions = await client.films_id_distributions_get(id)

    for distribution in distributions:
        if (
            distribution["country"] is not None
            and distribution["country"].get("country") == "Россия"
            and distribution["type"] == "PREMIERE"
        ):
            premieres["premiere_ru"] = distribution["date"]
        if distribution["type"] == "WORLD_PREMIER":
            premieres["premiere_world"] = distribution["date"]

    return premieres


async def parse_kinopoisk(
    kinopoisk_film: dict, client: kinopoisk_client.KinopoiskClient
):
    id = kinopoisk_film["kinopoiskId"]

    filmcrew_id = 0  # TODO
    genres = ", ".join([genre["genre"] for genre in kinopoisk_film["genres"]])

    kinopoisk_id = kinopoisk_film["kinopoiskId"]
    imdb_id = kinopoisk_film["imdbId"]

    name_ru = kinopoisk_film["nameRu"]
    name_orig = kinopoisk_film["nameOriginal"]
    description = utils.parse_text(kinopoisk_film["description"])

    expenses = await get_budget_and_fees(id, client)

    duration = kinopoisk_film["filmLength"]

    rating_kinopoisk = kinopoisk_film["ratingKinopoisk"]
    rating_imdb = kinopoisk_film["ratingImdb"]
    rating_kinorepa = None

    release_year = kinopoisk_film["year"]

    premieres = await get_premieres(id, client)
    premiere_ru = premieres.get("premiere_ru")
    premiere_world = premieres.get("premiere_world")

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
        expenses,
        duration,
        rating_kinopoisk,
        rating_imdb,
        rating_kinorepa,
        release_year,
        premiere_ru,
        premiere_world,
        updated_at,
        published_at,
        poster_url,
    )


def parse_db(args):
    expenses = Expenses(
        budget=args[8],
        marketing=args[9],
        fees_ru=args[10],
        fees_usa=args[11],
        fees_world=args[12],
    )

    new_args = list(args[:8]) + [expenses] + list(args[13:])
    return Film(*new_args)
