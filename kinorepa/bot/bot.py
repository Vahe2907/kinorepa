# adding kinorepa directory
import sys

sys.path.append("../../kinorepa")

import aiogram
import datetime
from kinorepa.bot.utils import keyboard
from kinorepa import config
from kinorepa.database import manager as database_manager
from kinorepa.bot.utils import translations
from kinorepa.src import manager as kinorepa_manager

bot = aiogram.Bot(config.BOT_TOKEN)
bot_dispatcher = aiogram.Dispatcher(bot)

db_manager = database_manager.DBManager(config.DATABASE_NAME)


@bot_dispatcher.message_handler(commands=["reg"])
async def register(incoming_message: aiogram.types.Message):
    from_user = incoming_message.from_user

    if db_manager.is_user_registered(from_user.id):
        await incoming_message.answer(
            text=translations.get("already_registered"), parse_mode="markdown"
        )
    else:
        db_manager.register_user(
            from_user.id,
            from_user.mention,
            from_user.full_name,
            datetime.datetime.now(),
        )
        await incoming_message.answer(
            text=translations.get("successfully_registered"), parse_mode="markdown"
        )


@bot_dispatcher.message_handler(commands=["start", "help"])
async def introduction(incoming_message: aiogram.types.Message):
    from_user = incoming_message.from_user

    await incoming_message.answer(
        text=translations.get_with_args("introduction", from_user.first_name),
        parse_mode="markdown",
    )


@bot_dispatcher.message_handler(commands=["find"])
async def find(incoming_message: aiogram.types.Message):
    keyword = " ".join(incoming_message.text.split()[1:])

    film_ids = await kinorepa_manager.find_film_by_keyword(keyword)

    await create_listing_keyboard_by_ids(incoming_message, film_ids)


@bot_dispatcher.message_handler(commands=["get_liked"])
async def get_liked(incoming_message: aiogram.types.Message):
    from_user = incoming_message.from_user
    print(from_user.id)
    film_ids = db_manager.get_liked_films(from_user.id)

    if film_ids is None:
        film_ids = list()

    await create_listing_keyboard_by_ids(incoming_message, film_ids)


@bot_dispatcher.message_handler(commands=["get_to_watch"])
async def get_to_watch(incoming_message: aiogram.types.Message):
    from_user = incoming_message.from_user
    film_ids = db_manager.get_to_watch_films(from_user.id)

    if film_ids is None:
        film_ids = list()

    await create_listing_keyboard_by_ids(incoming_message, film_ids)


async def create_listing_keyboard_by_ids(
    incoming_message: aiogram.types.Message, film_ids
):
    if len(film_ids) == 0:
        await incoming_message.answer(
            text=translations.get("nothing_found"), parse_mode="markdown"
        )
        return

    current_film = await kinorepa_manager.find_film_by_id(film_ids[0], db_manager)
    await incoming_message.answer(
        text=current_film,
        parse_mode="markdown",
        reply_markup=keyboard.create_films_keyboard(0, film_ids),
    )


@bot_dispatcher.callback_query_handler(
    lambda callback_query: callback_query.data == "liked"
)
async def callback_liked(callback_query: aiogram.types.CallbackQuery):
    from_user = callback_query.from_user
    print(from_user.id)
    _, current_index, indexes = keyboard.parse_listing_callback_data(
        callback_query.message
    )
    current_film_id = indexes[current_index]
    db_manager.add_liked_film(from_user.id, current_film_id)


@bot_dispatcher.callback_query_handler(
    lambda callback_query: callback_query.data == "to_watch"
)
async def callback_to_watch(callback_query: aiogram.types.CallbackQuery):
    from_user = callback_query.message.from_user
    _, current_index, indexes = keyboard.parse_listing_callback_data(
        callback_query.message
    )
    current_film_id = indexes[current_index]
    db_manager.add_to_watch_film(from_user.id, current_film_id)


@bot_dispatcher.callback_query_handler(
    lambda callback_query: callback_query.data.split()[0] in ["flm|n", "flm|b"]
)
async def callback_films_listing(callback_query: aiogram.types.CallbackQuery):
    await keyboard.handle_films_listing(callback_query, bot, db_manager)


@bot_dispatcher.callback_query_handler(
    lambda callback_query: callback_query.data.split()[0] in ["fct|n", "fct|b"]
)
async def callback_facts_listing(callback_query: aiogram.types.CallbackQuery):
    await keyboard.handle_film_facts(callback_query, bot, db_manager)


@bot_dispatcher.callback_query_handler(
    lambda callback_query: callback_query.data == "facts"
)
async def callback_facts(callback_query: aiogram.types.CallbackQuery):
    message = callback_query.message
    _, current_index, indexes = keyboard.parse_listing_callback_data(
        callback_query.message
    )
    current_film_id = indexes[current_index]

    facts = await kinorepa_manager.find_facts_ids_by_film_id(
        current_film_id, db_manager
    )

    if not facts:
        await message.answer(
            text=translations.get("nothing_found"), parse_mode="markdown"
        )
        return

    current_fact = await kinorepa_manager.find_fact_by_id(facts[0], db_manager)
    await bot.send_message(
        chat_id=message.chat.id,
        text=current_fact,
        reply_markup=keyboard.create_facts_keyboard(0, facts),
        parse_mode="markdown",
    )


@bot_dispatcher.callback_query_handler(
    lambda callback_query: callback_query.data == "genre"
)
async def callback_genre(callback_query: aiogram.types.CallbackQuery):
    await keyboard.filter_films_listing(callback_query, bot)


@bot_dispatcher.callback_query_handler(
    lambda callback_query: callback_query.data == "year"
)
async def callback_genre(callback_query: aiogram.types.CallbackQuery):
    await keyboard.filter_films_listing(callback_query, bot)


@bot_dispatcher.callback_query_handler(
    lambda callback_query: callback_query.data == "duration"
)
async def callback_genre(callback_query: aiogram.types.CallbackQuery):
    await keyboard.filter_films_listing(callback_query, bot)


@bot_dispatcher.callback_query_handler(
    lambda callback_query: callback_query.data == "rating_kp"
)
async def callback_genre(callback_query: aiogram.types.CallbackQuery):
    await keyboard.filter_films_listing(callback_query, bot)


@bot_dispatcher.callback_query_handler(
    lambda callback_query: callback_query.data == "rating_imdb"
)
async def callback_genre(callback_query: aiogram.types.CallbackQuery):
    await keyboard.filter_films_listing(callback_query, bot)


@bot_dispatcher.message_handler(commands=["filters"])
async def choose_filters(incoming_message: aiogram.types.Message):

    await incoming_message.answer(
        text="Выберите фильтр",
        reply_markup=keyboard.filter_keyboard("start_find"),
    )


if __name__ == "__main__":
    aiogram.executor.start_polling(bot_dispatcher, skip_updates=True)
