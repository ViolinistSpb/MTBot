import re

# Исходный текст
text = """
Вс 16.02.2025 
12:30 - 13:30 М2, основная сцена Орк. реп. Волшебная флейта лит.р. (11:34 М2, 1й служебный вход)14:00 - 17:20 Факт:14:07 - 17:31 М2, основная сцена Волшебная флейта (11:34 М2, 1й служебный вход)
Пн 17.02.2025 
Выходной (17.02.2025 - 17.02.2025)
Вт 18.02.2025 
17:15 - 18:30 М3, основная сцена Орк. реп. Фальстаф (п.с.)19:00 - 21:40 М3, основная сцена Фальстаф (п.с.)
Ср 19.02.2025 
Выходной (19.02.2025 - 19.02.2025) Не занимать (19.02.2025 - 19.02.2025) Не занимать (19.02.2025 - 19.02.2025) Не занимать (19.02.2025 - 19.02.2025)
Чт 20.02.2025 
14:00 - 16:45 М3, основная сцена Орк. реп. Сорочинская ярмарка к.и.
Пт 21.02.2025 
17:00 - 18:30 М3, основная сцена Орк. реп. Сорочинская ярмарка к.и.19:00 - 21:15 М3, основная сцена Сорочинская ярмарка к.и.
"""

# Регулярное выражение для удаления скобок и их содержимого
pattern = r"\([^()]*\)"

# Удаляем скобки и их содержимое
result = re.sub(pattern, "", text)

# Убираем лишние пробелы и переносы строк
result = re.sub(r"\s+", " ", result).strip()

print(result)