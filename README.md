# Telegram Weather Bot

Этот бот для Telegram предоставляет прогноз погоды и поддерживает подписку на ежедневные уведомления.

# Функциональность

Получение текущего и завтрашнего прогноза погоды по введенному городу.

Подписка на ежедневные уведомления о погоде в 8 утра.

Управление подпиской с помощью команд.

# Установка

1. Клонирование репозитория
   git clone https://github.com/picosiki/weather_bot.git
   cd weather-bot
3. Установка зависимостей
   pip install -r requirements.txt
4. Настройка
Создайте файл modules/my_config.py и добавьте в него:
class Config:
    BOT_TOKEN = "your_telegram_bot_token"
    WEATHER_API_KEY = "your_openweathermap_api_key"
# Запуск бота
  python bot.py
# Команды бота
/start – Начало работы и получение прогноза погоды.
/help – Список доступных команд.
/subscribe – Подписка на ежедневные уведомления о погоде.
/unsubscribe – Отписка от ежедневных уведомлений.

# Технологии
Python + aiogram
SQLite для хранения подписчиков
OpenWeatherMap API для получения погоды

# Cтруктура проекта
weather-bot/
│── bot.py              # Основной файл бота
│── requirements.txt    # Зависимости
│── modules/
│   ├── my_config.py    # Конфигурация бота
│── weather_bot.db      # База данных подписчиков

