import re


def remove_html_tags(text):
    clean1 = re.compile(r"<[^>]+>")
    clean2 = re.compile(r"&#\d*;")

    text = re.sub(clean1, "", text)
    text = re.sub(clean2, '"', text)

    return text


def parse_text(text):
    if text is None:
        return None

    text = remove_html_tags(text)

    text = text.replace("&laquo;", '"')
    text = text.replace("&raquo;", '"')

    text = text.replace("`", "'")
    text = text.replace("_", "-")
    text = text.replace("*", "^")

    return text


def date_to_str(date):
    months = [
        "янв.",
        "февр.",
        "марта",
        "апр.",
        "мая",
        "июня",
        "июля",
        "авг.",
        "сент.",
        "окт.",
        "нояб.",
        "дек.",
    ]

    return f"{date.day} {months[date.month - 1]} {date.year}"
