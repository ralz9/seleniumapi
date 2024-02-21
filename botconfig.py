# Импортируем необходимые модули
import requests
from decouple import config

# Объявляем переменные перед функцией
api_token = config('TOKEN')
chat_id = None
last_update_id = None

def func_send_message(chat_id, text_message):
    requests.post(f'https://api.telegram.org/bot{api_token}/sendMessage', json={'chat_id': chat_id, 'text': text_message})





def func_requests_tg_api():
    global chat_id, last_update_id  # Используем global для доступа к переменным извне функции
    response = requests.get(f'https://api.telegram.org/bot{api_token}/getUpdates', params={'offset': last_update_id})

    updates = response.json()['result']
    if updates:
        for update in updates:
            message = update.get('message')
            if message:
                chat_id = message['chat']['id']
                message_text = message.get('text')
                last_update_id = update['update_id'] + 1
                print(message_text)
                if message_text == '/stop':
                    
                    func_send_message(chat_id, 'Парсер успешно остановен для запуска /p')
                    return True

                elif message_text == '/info':
                    func_send_message(chat_id, 'Парсер работает,  для скриншота /screen')
                      
                elif message_text == '/screen':
                    func_send_message(chat_id, 'скриншот!!!!')
                    return ['screen', chat_id]

def func_send_file(files, data):
    requests.post(f'https://api.telegram.org/bot{api_token}/sendPhoto', files=files, data=data)
    








# Вызываем функцию
# while True:
#     if func_requests_tg_api() == True:
#         print('zxxzx')

# # Переменные chat_id и last_update_id могут быть доступны здесь после вызова функции
# print(chat_id)
# print(last_update_id)
