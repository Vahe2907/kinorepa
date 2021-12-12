import pytest

from kinorepa.kinopoisk_api import kinopoisk_client


client = kinopoisk_client.KinopoiskClient("f83fc52f-813a-437e-8e4a-560bd3ddcb74")


async def test_films_id_get():
    film = await client.films_id_get(263531)

    film.pop("lastSync")
    assert film == {
        "completed": False,
        "countries": [{"country": "США"}],
        "description": "Локи, сводный брат Тора, возвращается, и в этот раз он не "
        "один. Земля оказывается на грани порабощения, и только лучшие "
        "из лучших могут спасти человечество. Глава международной "
        "организации Щ.И.Т. Ник Фьюри собирает выдающихся поборников "
        "справедливости и добра, чтобы отразить атаку. Под "
        "предводительством Капитана Америки Железный Человек, Тор, "
        "Невероятный Халк, Соколиный Глаз и Чёрная Вдова вступают в "
        "войну с захватчиком.",
        "editorAnnotation": None,
        "endYear": None,
        "filmLength": 137,
        "genres": [
            {"genre": "фантастика"},
            {"genre": "приключения"},
            {"genre": "боевик"},
            {"genre": "фэнтези"},
        ],
        "has3D": True,
        "hasImax": True,
        "imdbId": "tt0848228",
        "isTicketsAvailable": False,
        "kinopoiskId": 263531,
        "nameEn": None,
        "nameOriginal": "The Avengers",
        "nameRu": "Мстители",
        "posterUrl": "https://kinopoiskapiunofficial.tech/images/posters/kp/263531.jpg",
        "posterUrlPreview": "https://kinopoiskapiunofficial.tech/images/posters/kp_small/263531.jpg",
        "productionStatus": None,
        "ratingAgeLimits": "age12",
        "ratingAwait": 93.78,
        "ratingAwaitCount": 54443,
        "ratingFilmCritics": 8.1,
        "ratingFilmCriticsVoteCount": 362,
        "ratingGoodReview": 82.3,
        "ratingGoodReviewVoteCount": 541,
        "ratingImdb": 8.0,
        "ratingImdbVoteCount": 1317607,
        "ratingKinopoisk": 7.9,
        "ratingKinopoiskVoteCount": 516927,
        "ratingMpaa": "pg13",
        "ratingRfCritics": 83.3333,
        "ratingRfCriticsVoteCount": 18,
        "reviewsCount": 705,
        "serial": False,
        "shortDescription": "Команда супергероев дает отпор скандинавскому богу Локи. "
        "Начало фантастической саги в киновселенной Marvel",
        "shortFilm": False,
        "slogan": "Avengers Assemble!",
        "startYear": None,
        "type": "FILM",
        "webUrl": "https://www.kinopoisk.ru/film/263531/",
        "year": 2012,
    }
