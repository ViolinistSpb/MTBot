import re
from diff_match_pacth import diff_match_patch


def validate_email(email):
    pattern = r"^[A-Za-z.]{2,20}$"
    return bool(re.match(pattern, email))


def validate_password(password):
    pattern = r"^[^\u0400-\u04FF]{1,30}$"
    return bool(re.match(pattern, password))


def clean_text(text):
    words_to_remove = ["Первые скрипки", "Вторые скрипки", "Альты", "Оркестр",
                       "Репетиция", "Спектакль", "Виолончели", "Контрабасы"]
    for word in words_to_remove:
        text = text.replace(word, "")
    text = text.replace(r"\([^()]*\)", "")
    text = re.sub(r"(?<=[^\s])([А-Я])", r" \1", text)
    text = re.sub(r"(Оркестр)(?!\n)", r"\1", text)
    return text


def add_markdown(text):
    pattern = r"([А-Я][а-я]) (\d{2}\.\d{2}\.\d{4})"
    text = re.sub(pattern, r"\n<b>\1 \2</b>", text)  # add \n
    pattern = r"(\d{2}:\d{2})( - )(\d{2}:\d{2})"
    text = re.sub(pattern, r"<i>\1\2\3</i>", text)
    pattern = r"([MМ][123])"
    text = re.sub(pattern, r"<b><i>\1</i></b>", text)
    text = re.sub(r"Гастроли", r"🚀Гастроли", text)
    text = re.sub(r"Выходной", r"🎉Выходной", text)
    return text


def diff_func(text1, text2):
    dmp = diff_match_patch()
    diff = dmp.diff_main(text1, text2)
    dmp.diff_cleanupSemantic(diff)
    result = ''
    for op, data in diff:
        if op == -1:
            result += f"Удалено: {data}\n"
        elif op == 1:
            result += f"Добавлено: {data}"
    return result


# text1 = '122345 sdflkhglkgh lihg'
# text2 = '122345 abc hhhhh'
# diff = diff_func(text1, text2)
# print(diff)
