# while_bool = True

# def func():
#     global while_bool
#     while_bool = False

# func()
# print(while_bool)

from decouple import config
import requests

api_token = config('TOKEN')

try:
    chat_id_in_env = config('CHATID')
    chat_id_in_env_list = chat_id_in_env.split(',')
    for ch in chat_id_in_env_list:
        requests.post(f'https://api.telegram.org/bot{api_token}/sendMessage', json={'chat_id': ch.strip(), 'text': 'Перезапустите парсер'})
except Exception as ex:
    print(ex)