import os
import shutil
import time

import requests
from loguru import logger
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from parser.utilities import xpaths
from parser.utilities.system_config import *


def try_download_image(img_url, path_to_save, file_name):
    logger.info(f'Попытка скачать: {img_url}')

    file_name += '.' + img_url.split('.')[-1]

    # получение изображения
    r = requests.get(img_url, stream=True, verify=False)
    r.raise_for_status()
    r.raw.decode_content = True  # support Content-Encoding e.g., gzip

    # создание папки для сохранения фото
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)

    # сохранение изображения
    with open(os.path.join(path_to_save, file_name), 'wb') as file:
        shutil.copyfileobj(r.raw, file)

    logger.info(f'Изображение {img_url} было успешно скачано в директорию {os.path.join(path_to_save, file_name)}')


def download_image(img_url, path_to_save, file_name):
    for t in range(tries_to_download + 1):
        try:
            try_download_image(img_url, path_to_save, file_name)
            break
        except Exception as error:
            if t == tries_to_download:
                raise error
            time.sleep(time_to_wait_before_download_image)
