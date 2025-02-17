import subprocess
import time

# Запускаем два процесса и сохраняем ссылки на них
proc1 = subprocess.Popen(["python3", "updation.py"])
proc2 = subprocess.Popen(["python3", "asus_bot.py"])

try:
    while True:
        time.sleep(1)  # Бесконечный цикл, пока не прервешь вручную (Ctrl+C)
except KeyboardInterrupt:
    print("Остановка процессов...")
    proc1.terminate()  # Остановка первого процесса
    proc2.terminate()  # Остановка второго процесса
    proc1.wait()  # Дожидаемся завершения
    proc2.wait()
    print("Процессы остановлены.")
