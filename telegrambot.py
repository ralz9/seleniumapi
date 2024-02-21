
import requests
import json
import time
from loguru import logger

from config import waiting_time, small_waiting_time, login, password
from main import update_reviews
from parser import Parser
from decouple import config
from botconfig import func_send_message



# Здесь вы можете указать свой токен бота
api_token = config('TOKEN')

chat_id = None
text = None

def check_new_messages():
    global  chat_id, text
    text_start = 'Hello дял запуска /p'
    text_p = 'Запуск парсера'
    last_update_id = None



    while True:
        try:
            # Запрос к API Telegram для получения обновлений
            response = requests.get(f'https://api.telegram.org/bot{api_token}/getUpdates',
                                    params={'offset': last_update_id} ) 

            updates = response.json()['result']

            if updates:
                # Обрабатываем каждое обновление
                for update in updates:
                    # print(update)
                    message = update.get('message')
                    if message:
                        # Получаем информацию о сообщении
                        text = message.get('text')
                        chat_id = message['chat']['id']

                        # Выводим информацию о сообщении
                        print(f"Received new message: '{text}' from chat_id: {chat_id}")
                        last_update_id = update['update_id'] + 1
                        if text == '/start':
                            func_send_message(chat_id , text_start)
                            last_update_id = update['update_id'] + 1
                        elif text == '/p':
                            logger.info('Запуск парсера')
                            
                            func_send_message(chat_id , text_p)

                            parser = Parser(waiting_time, small_waiting_time, login, password)
                            last_update_id = update['update_id'] + 1
                            parser.login(last_update_id, chat_id)
                            while True:
                                update_reviews(parser, last_update_id,  chat_id)
                        elif text == '/info':
                            func_send_message(chat_id , 'Парсер Не запущен!!!!!')
                        elif text == '/stop':
                            func_send_message(chat_id , 'Парсер  не запущен!!!!!!! ')
                        elif text == '/screen':
                            func_send_message(chat_id , 'Скриншот не возможен Парсер не запущен!!!!!')


                        # Подготовка к следующему запросу


            # Задержка перед следующим запросом, чтобы не создавать большую нагрузку
            time.sleep(1)

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    check_new_messages()
