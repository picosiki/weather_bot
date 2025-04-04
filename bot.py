import asyncio
import aiohttp
import sqlite3
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from datetime import datetime, timedelta, timezone
import os

DB_PATH = "weather_bot.db"
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

# Инициализация базы данных
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                user_id INTEGER PRIMARY KEY
            )
        """)
        conn.commit()

init_db()

# Функции работы с БД
def add_subscriber(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO subscribers (user_id) VALUES (?)", (user_id,))
        conn.commit()

def remove_subscriber(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subscribers WHERE user_id = ?", (user_id,))
        conn.commit()

def get_subscribers():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM subscribers")
        return [row[0] for row in cursor.fetchall()]

# Функция получения локального времени
def convert_utc_to_local(utc_timestamp, timezone_offset):
    local_time = datetime.fromtimestamp(utc_timestamp, timezone.utc) + timedelta(seconds=timezone_offset)
    return local_time

# Функция получения погоды
async def get_weather(city):
    global session
    try:
        url_today = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
        url_forecast = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
        
        async with session.get(url_today) as response:
            data_today = await response.json()
        async with session.get(url_forecast) as response:
            data_forecast = await response.json()
        
        if "main" not in data_today or "list" not in data_forecast:
            return "Ошибка: не могу получить погоду."
        
        timezone_offset = data_today.get("timezone", 0)
        temp_today = data_today["main"]["temp"]
        wind_today = data_today["wind"]["speed"]
        desc_today = data_today["weather"][0]["description"].capitalize()
        
        today_local_time = convert_utc_to_local(datetime.now(timezone.utc).timestamp(), timezone_offset)
        today_local_time_str = today_local_time.strftime("%Y-%m-%d %H:%M:%S")
        
        temp_tomorrow, wind_tomorrow, desc_tomorrow = "Нет данных", "Нет данных", "Нет данных"
        tomorrow_time_str = "Нет данных"
        
        forecast = data_forecast["list"][6]
        temp_tomorrow = forecast["main"]["temp"]
        wind_tomorrow = forecast["wind"]["speed"]
        desc_tomorrow = forecast["weather"][0]["description"].capitalize()
        tomorrow_time = convert_utc_to_local(forecast["dt"], timezone_offset)
        tomorrow_time_str = tomorrow_time.strftime("%Y-%m-%d %H:%M:%S")
                
        
        return (
            f"Погода в {city}:\n"
            f"Сегодня ({today_local_time_str}): {temp_today}°C,\nВетер: {wind_today} м/с, {desc_today}\n"
            f"Завтра ({tomorrow_time_str}): {temp_tomorrow}°C,\nВетер: {wind_tomorrow} м/с, {desc_tomorrow}"
        )
    except Exception as e:
        return f"Ошибка получения данных: {str(e)}"

# Автоуведомления в 8 утра
async def daily_weather_notifications():
    while True:
        now = datetime.now()
        next_run = datetime(now.year, now.month, now.day, 8, 0, 0)
        if now > next_run:
            next_run += timedelta(days=1)
        wait_time = (next_run - now).total_seconds()
        await asyncio.sleep(wait_time)
        weather_info = await get_weather("Москва")
        for user_id in get_subscribers():
            await bot.send_message(user_id, weather_info)

# Команды
@dp.message(Command("help"))
async def start_command(message: Message):
    await message.answer("/subscribe подписка на рассылку погоды /unsubscribe отписка /start - получить прогноз")

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("/subscribe подписка на рассылку погоды /unsubscribe отписка /help помощь\nВведи название города, чтобы получить погоду")

@dp.message(Command("subscribe"))
async def subscribe_user(message: Message):
    add_subscriber(message.from_user.id)
    await message.answer("Вы подписались на ежедневную рассылку погоды!")

@dp.message(Command("unsubscribe"))
async def unsubscribe_user(message: Message):
    remove_subscriber(message.from_user.id)
    await message.answer("Вы отписались от рассылки погоды.")

@dp.message()
async def send_weather(message: Message):
    city = message.text.strip()
    weather_info = await get_weather(city)
    await message.answer(weather_info)

# Запуск бота
async def main():
    global session
    session = aiohttp.ClientSession()
    asyncio.create_task(daily_weather_notifications())
    try:
        await dp.start_polling(bot)
    finally:
        await session.close()

if __name__ == "__main__":
    asyncio.run(main())
