import datetime


class Film:
    """
    Фильм

    Поля:
      - id: int (уникальный идентификатор)

      - filmcrew_id: int (идентификатор съёмочной команды)
      - genre: str (жанр фильма)

      - kinopoisk_id: int (идентификатор фильма в Кинопоиске)
      - imdb_id: int (идентификатор фильма в Imdb)

      - name_ru: str (название фильма на русском)
      - name_en: str (название фильма на английском)
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
        genre: str,
        kinopoisk_id: int,
        imdb_id: int,
        name_ru: str,
        name_en: str,
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
    ):
        self._id = id

        self._filmcrew_id = filmcrew_id
        self._genre = genre

        self._kinopoisk_id = kinopoisk_id
        self._imdb_id = imdb_id

        self._name_ru = name_ru
        self._name_en = name_en
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


def _get_film_by_kinopoisk_id(kinopoisk_id: int):
    pass
