import aiohttp
import asyncio
from modules.my_config import Config

config = Config()
WEATHER_API_KEY = config.WEATHER_API_KEY
async def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    if "main" in data:
        temp = data["main"]["temp"]
        wind_speed = data["wind"]["speed"]
        weather_desc = data["weather"][0]["description"].capitalize()
        return f" Погода в {city}:\n Температура: {temp}°C\n Ветер: {wind_speed} м/с\n {weather_desc}"
    else:
        return "Ошибка: не могу получить погоду."
    

# Добавляем точку входа в программу
async def main():
    city = config.USER_CITY  # Замените на нужный город
    weather_info = await get_weather(city)
    print(weather_info)

# Запуск основного цикла событий
if __name__ == "__main__":
    asyncio.run(main())
    