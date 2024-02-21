import requests

from loguru import logger
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions
import asyncio
from parser.utilities import xpaths
from parser.utilities.system_config import *
import os
from decouple import config
from botconfig import func_send_message, func_requests_tg_api


def enter_captcha( wait, browser, last_update_id, chat_id):
    func_requests_tg_api()
    if func_requests_tg_api() == True:
        browser.close()

    api_token = config('TOKEN')

    # в capthca_text будет храниться объект отправленный пользователем в телеграме
    captcha_text = None

    # last id это идентификатор для того чтобы вытаскивать последние сообщени с request
    last_id = None

    last_update_id = last_update_id




    while True:
        # print(message)
        browser.get_screenshot_as_file("screenshot.png")
        files = {'photo': open('screenshot.png', 'rb')}
        data = {'chat_id': chat_id}




        requests.post(f'https://api.telegram.org/bot{api_token}/sendPhoto', files=files, data=data)


  

        func_send_message(chat_id, 'Введите капчу!!!')






        while not captcha_text:

            try:
                # Запрос к API Telegram для получения обновлений
                response = requests.get(f'https://api.telegram.org/bot{api_token}/getUpdates',
                                        params={'offset': last_update_id})

                updates = response.json()['result']
                print(response.json(), 'response.json()')
                if updates:

                    # Обрабатываем каждое обновление
                    for update in updates:
                        print(update)

                        # if update['update_id'] == last_update_id:
                        message = update.get('message')
                        print('message')

                        if message:
                            captcha_text = (message.get('text'))
                            last_id = update['update_id'] + 1
                            last_update_id = last_id
                if captcha_text == '/stop':
                    browser.close()

            except Exception as ex:
                print(ex)

        # captcha_text = input('Введите капчу')

        logger.info('Отправка капчи')
        func_send_message(chat_id, 'Отправка капчи')
        captcha_line = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.captcha_line)))
        captcha_line.send_keys(captcha_text)
        captcha_line.send_keys(Keys.ENTER)

        # проверка на успешность ввода капчи
        logger.info('Проверка на успешность ввода')
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.captcha_img)))
            logger.error('Капча введена неудачно')
            func_send_message(chat_id, 'Капча введена неудачно !!!!')
            captcha_text = None
        except exceptions.TimeoutException:
            logger.info('Капча введена успешно')
            func_send_message(chat_id, 'Капча введена успешно !!!! !!!!')
            break

    # Ввод неверных данных для входа, для корректного нахождения xpath-ов

    # капча
    login_captcha_line = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.first_login_captcha_line)))
    login_captcha_line.send_keys('captcha')

    # логин
    username_line = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.first_login_username_line)))
    username_line.send_keys('username')

    # пароль
    password_line = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.first_login_password_line)))
    password_line.send_keys('password')

    # переход дальше
    accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.login_accept_button)))
    accept_button.click()


def enter_username_and_password(wait, username, password, browser, chat_id, last_update_id):
    func_requests_tg_api()
    if func_requests_tg_api() == True:
        browser.close()

        
    captcha_text = None

    # last id это идентификатор для того чтобы вытаскивать последние сообщени с request
    last_id = None

    last_update_id = last_update_id + 1

    api_token = config('TOKEN')

    while True:
        logger.info('Отправка логина и пароля')

        # ввод логина
        username_line = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.login_username_line)))
        username_line.send_keys(username)

        # ввод пароля
        password_line = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.login_password_line)))
        password_line.send_keys(password)

        # ввод капчи
        browser.get_screenshot_as_file("screenshot.png")
        files = {'photo': open('screenshot.png', 'rb')}
        data = {'chat_id': chat_id}



        requests.post(f'https://api.telegram.org/bot{api_token}/sendPhoto', files=files, data=data)


      

        func_send_message(chat_id, 'Введите капчу для логина!!!')








        while not captcha_text:

            try:
                # Запрос к API Telegram для получения обновлений
                response = requests.get(f'https://api.telegram.org/bot{api_token}/getUpdates',
                                        params={'offset': last_update_id})

                updates = response.json()['result']
                print(response.json(), 'response.json()')
                if updates:

                    # Обрабатываем каждое обновление
                    for update in updates:
                        print(update)

                        # if update['update_id'] == last_update_id:
                        message = update.get('message')
                        print('message')

                        if message:
                            captcha_text = (message.get('text'))
                            last_id = update['update_id'] + 1
                            last_update_id = last_id

            except Exception as ex:
                print(ex)



        if captcha_text == '/stop':
            browser.close()

        logger.info('Отправка капчи')
      

        func_send_message(chat_id, 'Отправка капчи!!!')
        captcha_line = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.login_captcha_line)))
        captcha_line.send_keys(captcha_text)

        accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.login_accept_button)))
        accept_button.click()

        logger.info('Проверка на успешность ввода')

        if not browser.find_elements(By.CSS_SELECTOR, "[class='flex border px-3 py-2 rounded-xl border-red-500 bg-red-50 mb-2 w-full']"):

            func_send_message(chat_id, 'Успешно!!!!!')
            break
        else:
            
            func_send_message(chat_id, 'Повторная попытка входа после неудачной капчи!!!!!!!!')

            logger.info('Повторная попытка входа после неудачной капчи.')
            captcha_text = None



        # try:
        #     wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.login_captcha_img)))
        #     logger.error('Капча введена неудачно')
        # except exceptions.TimeoutException:
        #     logger.info('Капча введена успешно')
        #     break


def login(browser, wait, username, password, last_update_id, chat_id):
    # send_photo_captcha(message)
    browser.get(main_url)
    enter_captcha(wait, browser, last_update_id, chat_id)
    enter_username_and_password(wait, username, password, browser, chat_id, last_update_id)
