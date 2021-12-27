# adding kinorepa directory
import sys

sys.path.append("../../kinorepa")

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import typing

from kinorepa.src import manager as kinorepa_manager

genres_ = [
    "Боевик",
    "Комедии",
    "Мультфильмы",
    "Ужасы",
    "Фантастика",
    "Триллеры",
    "Приключения",
    "Детектив",
    "Аниме",
]
years_ = ["До 1990", "1990 - 2000 гг.", "2000 - 2010 гг.", "После 2010"]
durations_ = ["До 90 мин", "90 - 120 мин", "120 - 150 мин", "Более 150 мин"]
rating_kp = ["< 4", "4 - 6", "6 - 8", "8 - 10"]
rating_imdb = ["< 4", "4 - 6", "6 - 8", "8 - 10"]
duration_to_segment = {
    ("До 90 мин", (0, 90)),
    ("90 - 120 мин", (90, 120)),
    ("120 - 150 мин", (120, 150)),
    ("Более 150 мин", (150, 1000))
}
years_to_segment = {
    ("До 1990", (0, 1990)),
    ("1990 - 2000 гг.", (1990, 2000)),
    ("2000 - 2010 гг.", (2000, 2010)),
    ("После 2010", (2010, 2100)),
}


def _add_back_next_buttons(
    prefix: str,
    current_index: int,
    indexes: typing.List[int],
    inline_kb: InlineKeyboardMarkup,
):
    left_indexes = " ".join([str(index) for index in indexes[:6]])
    right_indexes = " ".join([str(index) for index in indexes[6:13]])

    left_data = f"{prefix}|b {current_index} {left_indexes}"
    right_data = f"{prefix}|n {current_index} {right_indexes}"

    kb_back = InlineKeyboardButton("<<", callback_data=left_data)
    kb_next = InlineKeyboardButton(">>", callback_data=right_data)

    inline_kb.add(kb_back, kb_next)


def create_films_keyboard(
    current_index: int,
    indexes: typing.List[int],
) -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup()

    _add_back_next_buttons("flm", current_index, indexes, inline_kb)

    kb_like = InlineKeyboardButton("Мне нравится! 🧡", callback_data="liked")
    kb_to_watch = InlineKeyboardButton(
        "Добавить в «Смотреть позже»!", callback_data="to_watch"
    )
    kb_interesting_facts = InlineKeyboardButton(
        "Интересные факты 💥", callback_data="facts"
    )
    kb_similars = InlineKeyboardButton("Похожие фильмы 🎥", callback_data="similars")

    inline_kb.add(kb_interesting_facts)
    inline_kb.add(kb_like)
    inline_kb.add(kb_to_watch)
    inline_kb.add(kb_similars)

    return inline_kb


def create_facts_keyboard(
    current_index: int,
    indexes: typing.List[int],
):
    inline_kb = InlineKeyboardMarkup()

    _add_back_next_buttons("fct", current_index, indexes, inline_kb)

    return inline_kb


def filter_keyboard(name):
    inline_kb = InlineKeyboardMarkup()
    global genres_, years_, durations_, rating_kp, rating_imdb
    if name == "start_find":
        genres = InlineKeyboardButton("Жанр", callback_data="genre")
        year = InlineKeyboardButton("Год выпуска", callback_data="year")
        duration = InlineKeyboardButton("Длительность", callback_data="duration")
        actors = InlineKeyboardButton("Актеры", callback_data="actors")
        find = InlineKeyboardButton("Поиск!", callback_data="find_res")
        rating_kp = InlineKeyboardButton(
            "Рейтинг (Кинопоиск)", callback_data="rating_kp"
        )
        rating_imdb = InlineKeyboardButton(
            "Рейтинг (IMDB)", callback_data="rating_imdb"
        )
        budget = InlineKeyboardButton("Бюджет", callback_data="_budget")
        collection = InlineKeyboardButton("Кассовые сборы", callback_data="collection")

        inline_kb.add(genres, year)
        inline_kb.add(duration, actors)
        inline_kb.add(rating_kp, rating_imdb)
        inline_kb.add(budget, collection)
        inline_kb.add(find)
        return inline_kb
    elif name == "genre":
        for genre in genres_:
            inline_kb.add(InlineKeyboardButton(genre, callback_data=genre))
    elif name == "year":
        for year in years_:
            inline_kb.add(InlineKeyboardButton(year, callback_data=year))
    elif name == "duration":
        for dura in durations_:
            inline_kb.add(InlineKeyboardButton(dura, callback_data=dura))
    elif name == "rating_kp":
        for rat in rating_kp:
            inline_kb.add(InlineKeyboardButton(rat, callback_data=rat))
    elif name == "rating_imdb":
        for rat_imdb in rating_imdb:
            inline_kb.add(InlineKeyboardButton(rat_imdb, callback_data=rat_imdb))

    inline_kb.add(InlineKeyboardButton("Меню с фильтрами", callback_data="back"))
    return inline_kb


async def filter_films_listing(callback_query, bot):
    message = callback_query.message
    data = callback_query.data
    if data == "genre":
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text="Выберите жанр",
            reply_markup=filter_keyboard(data),
        )
    elif data == "year":
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text="Выберите год выпуска",
            reply_markup=filter_keyboard(data),
        )
    elif data == "duration":
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text="Выберите длительность фильма",
            reply_markup=filter_keyboard(data),
        )
    elif data == "rating_kp":
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text="Выберите рейтинг фильма на кинопоиске",
            reply_markup=filter_keyboard(data),
        )
    elif data == "rating_imdb":
        print(data)
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text="Выберите рейтинг фильма на IMDB",
            reply_markup=filter_keyboard(data),
        )


async def update_filters_set(callback_query, key_filter, db_manager):
    selected_filters = db_manager.find_user_filters(callback_query.from_user.id)
    print(selected_filters)
    if selected_filters is None:
        selected_filters = {}
    data = callback_query.data
    if key_filter not in selected_filters.keys():
        selected_filters[key_filter] = []
    if data in selected_filters[key_filter]:
        selected_filters[key_filter].remove(data)
    else:
        selected_filters[key_filter].append(data)
    db_manager.update_user_filters(callback_query.from_user.id, selected_filters)


def parse_listing_callback_data(message, data=None):
    left_button, right_buttton = message.reply_markup.inline_keyboard[0]

    if data is None:
        data = message.reply_markup.inline_keyboard[0][0].callback_data
    current_button, current_index = data.split()[0], int(data.split()[1])
    indexes = list(
        map(
            int,
            left_button.callback_data.split()[2:]
            + right_buttton.callback_data.split()[2:],
        )
    )

    return current_button, current_index, indexes


async def handle_films_listing(callback_query, bot, db_manager):
    data = callback_query.data
    message = callback_query.message

    current_button, current_index, indexes = parse_listing_callback_data(message, data)

    if current_button == "flm|n":
        next_index = current_index + 1
    elif current_button == "flm|b":
        next_index = current_index - 1
    else:
        raise RuntimeError()

    next_index %= len(indexes)
    if next_index == current_index:
        return

    next_film = await kinorepa_manager.find_film_by_id(indexes[next_index], db_manager)
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=next_film,
        reply_markup=create_films_keyboard(next_index, indexes),
        parse_mode="markdown",
    )


async def handle_film_facts(callback_query, bot, db_manager):
    data = callback_query.data
    message = callback_query.message

    current_button, current_index, indexes = parse_listing_callback_data(message, data)

    if current_button == "fct|n":
        next_index = current_index + 1
    elif current_button == "fct|b":
        next_index = current_index - 1
    else:
        raise RuntimeError()

    next_index %= len(indexes)
    if next_index == current_index:
        return

    next_film = await kinorepa_manager.find_fact_by_id(indexes[next_index], db_manager)
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=next_film,
        reply_markup=create_facts_keyboard(next_index, indexes),
        parse_mode="markdown",
    )
