# -*- coding: UTF-8 -*-
import os
import codecs
from dotenv import load_dotenv
#Подключаем модуль для работы с yaml
try:
    import yaml
except ImportError as error:
    print("pip install pyyaml")
    exit()

class Config:
    def __init__(self):
        #Определяем рабочую директорию
        self.__path = os.path.dirname(os.path.realpath(__file__)) + "/../conf/"

        #Инициация основного конфига
        with codecs.open(self.__path + "config.yaml", 'rb') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

        self.USER_CITY = cfg['CONFIG']['DEFAULT_CITY']

        # Загружаем переменные окружения из .env
        dotenv_path = os.path.join(os.path.dirname(__file__), '../conf/.env')
        # Загружаем переменные окружения
        load_dotenv(dotenv_path)
        self.BOT_TOKEN = os.getenv('BOT_TOKEN')
        self.WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')