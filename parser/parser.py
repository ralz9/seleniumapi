import json
import os
import traceback
from pprint import pprint


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio
from loguru import logger

from parser.utilities import image_utils, login_utils, links_utils, goods_utils
from decouple import config
from botconfig import *
import requests




class Parser:
    def __init__(self, waiting_time, small_waiting_time, username, password):
        self.api_token = config('TOKEN')
        self.last_update_id = None
        # открытие браузера
        options = Options()
        options.add_argument('--headless')
        # self.__browser = webdriver.Chrome(options=options)
        self.__browser = webdriver.Chrome()
        # настройка времени ожидания загрузки элемента
        self.__wait = WebDriverWait(self.__browser, waiting_time)
        self.__wait_small = WebDriverWait(self.__browser, small_waiting_time)
        # сохранение логина и пароля
        self.__username = username
        self.__password = password
        func_requests_tg_api()
        logger.info('Браузер успешно открыт и настроен')
        

    def login(self, last_update_id, chat_id):
        login_utils.login(self.__browser, self.__wait, self.__username, self.__password, last_update_id, chat_id)


    def get_stores_urls(self):
        func_req = func_requests_tg_api()
        # если команда в боте /stop парсер отсанавливается 
        if func_req == True:
            self.__browser.close()
        # если команда в боте /screen парсер делает скрин 
        elif isinstance(func_req, list) and func_req[0] == 'screen':
            self.__browser.get_screenshot_as_file("screenshot.png")
            files = {'photo': open('screenshot.png', 'rb')}
            data = {'chat_id': func_req[1]}
            requests.post(f'https://api.telegram.org/bot{api_token}/sendPhoto', files=files, data=data)
        # получение ссылок на все магазины
         # в данной переменной список из ссылок
        stores_urls = links_utils.get_stores_urls(self.__browser, self.__wait, )
        # записываем ссылки на магазины в файл
        with open('store_urls.json', 'w') as f:
            json.dump(stores_urls, f)
        logger.info(f'Получены ссылки на {len(stores_urls)} магазинов')
        return stores_urls


    # получение новых комментариев со всех товаров
    def get_new_reviews(self, store_url):
        # смотрим если есть капча значит произошел разлогин
        if self.__browser.find_elements(By.ID, "captcha-img"):
            self.__browser.close()

        # команда /stop в боте 
        func_req = func_requests_tg_api()
        if func_req == True:
            self.__browser.close()

        # проверяем евялется ли list так как передаем два значения саму команду screen и id пользователя 
        elif isinstance(func_req, list) and func_req[0] == 'screen':
            self.__browser.get_screenshot_as_file("screenshot.png")
            files = {'photo': open('screenshot.png', 'rb')}
            data = {'chat_id': func_req[1]}
            requests.post(f'https://api.telegram.org/bot{api_token}/sendPhoto', files=files, data=data)
            
                
        # получение ссылок на товары в магазинах
        goods_urls = links_utils.get_goods_urls(self.__browser, self.__wait, self.__wait_small, store_url)
        logger.info(f'Получены ссылки на {len(goods_urls)} товаров в магазине с id "{store_url.split("/")[-1]}"')
        



        reviews = {}

        # получение отзывов:
        for good_url in goods_urls:
            # проверяем если есть капча произошел разлогин 
            if self.__browser.find_elements(By.ID, "captcha-img"):
                self.__browser.close()

            logger.info(f'Получение отзывов для товара с id {good_url.split("/")[-1]}')

            # команда /stop  в боте
            func_req = func_requests_tg_api()
            if func_req == True:
                self.__browser.close()

            # проверяем евялется ли list так как передаем два значения саму команду screen и id пользователя 
            elif isinstance(func_req, list) and func_req[0] == 'screen':
                self.__browser.get_screenshot_as_file("screenshot.png")
                files = {'photo': open('screenshot.png', 'rb')}
                data = {'chat_id': func_req[1]}
                requests.post(f'https://api.telegram.org/bot{api_token}/sendPhoto', files=files, data=data)
                
                
            new_reviews = goods_utils.get_reviews(self.__browser, self.__wait, self.__wait_small, good_url)
            if new_reviews:
                reviews[good_url.split('/')[-1]] = new_reviews
            logger.debug(f'отзывы для товара "{good_url.split("/")[-1]}": {new_reviews}')

        return reviews
