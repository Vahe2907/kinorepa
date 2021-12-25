translations = {
    "introduction": (
        "Привет, {} 👋\n"
        "Я помогу тебе выбрать крутой фильм на вечер! Вот список доступных команд:\n"
        "  - */find* <_название_> - найти фильм\n"
    ),
    "nothing_found": "К сожалению, по твоему запросу не удалось ничего найти 😥",
}


def get(translation):
    return translations[translation]


def get_with_args(translation, *args):
    return translations[translation].format(*args)
