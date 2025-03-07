import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from modules.my_config import Config
from db import Database

config = Config()

# print(config.USER_CITY)
# print(config.BOT_TOKEN)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание объектов бота и диспетчера
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
db = Database()

db.create_tables()  # Создаём таблицы при запуске


@dp.message(Command("start"))
async def start_command(message: Message):
    user_id = message.from_user.id
    db.add_user(user_id)
    await message.answer("Привет! Я бот прогноза погоды. \nИспользуй /weather, чтобы узнать погоду.\nИспользуй /setcity Город, чтобы изменить город.")


@dp.message(Command("setcity"))
async def set_city_command(message: Message):
    user_id = message.from_user.id
    text = message.text.split(maxsplit=1)
    if len(text) < 2:
        await message.answer("Введите город после команды. Например: /setcity Москва")
        return
    city = text[1]
    db.update_city(user_id, city)
    await message.answer(f"✅ Город изменён на {city}")


@dp.message(Command("weather"))
async def weather_command(message: Message):
    user_id = message.from_user.id
    city = db.get_city(user_id) or config.USER_CITY
    weather_info = await get_weather(city)
    await message.answer(weather_info)


async def main():
    print("✅ Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
