import base64
import json

import requests
from loguru import logger

from config import *
from parser import Parser
import os
from decouple import config
import random

from botconfig import *

last_update_id = None
chat_id = None

def update_reviews(_parser, chat_id, last_update_id):
    logger.info('Запуск парсинга')
    text_count = None
    last_update_id = last_update_id
    chat_id = chat_id
    api_token = config('TOKEN')
    last_update_id = None
    
    
    



    try:
        check_file = os.path.getsize("store_urls.json")
    except Exception as ex:
        check_file = 2
    if os.path.isfile('store_urls.json') and check_file != 2:
        store = open('store_urls.json')
        stores_urls = json.load(store)
        random.shuffle(stores_urls)

        # print(stores_urls)
    else:
        _parser.get_stores_urls()
        store = open('store_urls.json')
        stores_urls = json.load(store)
        random.shuffle(stores_urls)



    for i, store_url in enumerate(stores_urls):
        new_reviews = _parser.get_new_reviews(store_url)
        logger.info(new_reviews)
        logger.info(f'Было спаршено: {i} магазинов')
        
        data_dict = {
            "token": "D38dlSmdjx3840sSs",
            "goods": []
        }

        for good in new_reviews:

            reviews_dict = []
            for review in new_reviews[good]:
                img_url = None
                img = None
                if review['img']:
                    img_url = review['img']
                    with open(f"icons\\{review['img']}", "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                    img = encoded_string.decode()

                reviews_dict.append(
                    {
                        "name": review['name'],
                        "text": review['text'],
                        "rating": int(review['rating']) if review['rating'] else None,
                        "purchase": review['purchase'],
                        "location": review['location'],
                        "date": review['date'],
                        "answer": review['answer'],
                        "img_url": img_url,
                        "img": img
                    }
                )

            data_dict['goods'].append({"good_id": good, "reviews": reviews_dict})

        logger.info(data_dict)
        logger.debug(json.dumps(data_dict))

# https://101.99.91.183/api/reviews/add/
        
        resp = requests.post(config('APIURL'),
                            headers={'Content-type': 'application/json'}, json=json.dumps(data_dict),
                            data=json.dumps(data_dict),
                            verify=False)

      

        logger.debug(f'Статус запросы: {resp.status_code}')


        if resp.status_code:
            logger.debug(f'- 1 ссылка успешно ')
            with open('store_urls.json', 'r') as f:
                json_list = json.load(f)
                json_list.remove(f'{store_url}')
                with open('store_urls.json', 'w') as file_temporary:
                    json.dump(json_list, file_temporary)

            
            

# if __name__ == '__main__':
#     logger.add('logs.txt')
#     logger.info('Запуск парсера')
#     parser = Parser(waiting_time, small_waiting_time, login, password)
#     parser.login(last_update_id, chat_id)
#     while True:
#         update_reviews(parser)
