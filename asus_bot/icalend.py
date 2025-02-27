from icalendar import Calendar, Event
from datetime import datetime
import pytz

cal = Calendar()

# Создаем событие
event = Event()
event.add('summary', 'Тестовое событие')
event.add('dtstart', datetime(2025, 2, 27, 11, 0, 0, tzinfo=pytz.utc))
event.add('dtend', datetime(2025, 2, 27, 12, 0, 0, tzinfo=pytz.utc))
event.add('description', 'Это тестовое событие для iCal.')

# Добавляем событие в календарь
cal.add_component(event)

# Сохраняем календарь в файл
with open('event.ics', 'wb') as f:
    f.write(cal.to_ical())

print("Файл event.ics создан.")