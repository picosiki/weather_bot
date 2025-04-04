# Используем официальный Python образ
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер, исключая то, что указано в .dockerignore
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт, на котором будет работать бот
EXPOSE 80

# Команда для запуска бота
CMD ["python", "bot.py"]
