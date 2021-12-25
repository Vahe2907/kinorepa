# adding kinorepa directory
import sys

sys.path.append("../../kinorepa")

import aiogram

from kinorepa import config
from kinorepa.database import manager as database_manager
from kinorepa.bot.utils import translations

from kinorepa.src import manager as kinorepa_manager


bot = aiogram.Bot(config.BOT_TOKEN)
bot_dispatcher = aiogram.Dispatcher(bot)

db_manager = database_manager.DBManager(config.DATABASE_NAME)


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

    film = await kinorepa_manager.find_by_keyword(keyword)

    if film is None:
        await incoming_message.answer(
            text=translations.get("nothing_found"), parse_mode="markdown"
        )
        return

    await incoming_message.answer(
        text=film,
        parse_mode="markdown",
    )


if __name__ == "__main__":
    aiogram.executor.start_polling(bot_dispatcher, skip_updates=True)
