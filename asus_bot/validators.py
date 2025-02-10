import re


def validate_email(email):
    pattern = r"^[A-Za-z.]{2,20}$"
    return bool(re.match(pattern, email))


def validate_password(password):
    pattern = r"^[^\u0400-\u04FF]{1,30}$"
    return bool(re.match(pattern, password))


def pre_clean_day(day):
    words_to_remove = ["Первые скрипки", "Вторые скрипки", "Альты", "Оркестр",
                       "Репетиция", "Спектакль"]
    for word in words_to_remove:
        day = day.replace(word, "")
    return day


def clean_day(day):
    day = re.sub(r"(?<=[^\s])([А-Я])", r" \1", day)
    day = re.sub(r"(Оркестр)(?!\n)", r"\1\n", day)
    pattern = r"([А-Я][а-я]) (\d{2}\.\d{2}\.\d{4})"
    day = re.sub(pattern, r"<b>\1 \2</b>", day)
    pattern = r"(\d{2}:\d{2})( - )(\d{2}:\d{2})"
    day = re.sub(pattern, r"<i>\1 \2 \3</i>", day)
    pattern = r"([MМ][123])"
    day = re.sub(pattern, r"<b><i>\1</i></b>", day)
    pattern = r"\([^()]*\)"
    day = day.replace(pattern, "")
    return day
