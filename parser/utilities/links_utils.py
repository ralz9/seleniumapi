from loguru import logger
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions

from parser.utilities import xpaths
from parser.utilities.system_config import page_url
from botconfig import *

def __get_stores_urls_on_page(wait, browser):

    func_req = func_requests_tg_api()
    if func_req == True:
        self.__browser.close()

    elif isinstance(func_req, list) and func_req[0] == 'screen':
        browser.get_screenshot_as_file("screenshot.png")
        files = {'photo': open('screenshot.png', 'rb')}
        data = {'chat_id': func_req[1]}
        requests.post(f'https://api.telegram.org/bot{api_token}/sendPhoto', files=files, data=data)

    urls = []

    # перебор всех магазинов на странице
    for store_num in range(1, 17):
        try:
            url = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.store_link.format(store_num=store_num)))).get_attribute('href')
            urls.append(url)
        except exceptions.TimeoutException:
            return urls

    return urls


def __get_goods_urls_on_page(wait, wait_small, browser):

    func_req = func_requests_tg_api()
    if func_req == True:
        self.__browser.close()

    elif isinstance(func_req, list) and func_req[0] == 'screen':
        browser.get_screenshot_as_file("screenshot.png")
        files = {'photo': open('screenshot.png', 'rb')}
        data = {'chat_id': func_req[1]}
        requests.post(f'https://api.telegram.org/bot{api_token}/sendPhoto', files=files, data=data)

    urls = []

    # ожидание полной загрузки страницы
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.good_link.format(good_num=1))))
    except exceptions.TimeoutException:
        return []

    # перебор всех товаров на странице
    for good_num in range(1, 19):
        try:
            url = wait_small.until(EC.element_to_be_clickable((By.XPATH, xpaths.good_link.format(good_num=good_num)))).get_attribute('href')
            urls.append(url)
        except exceptions.TimeoutException:
            return urls

    return urls


def get_stores_urls(browser, wait):
    func_req = func_requests_tg_api()
    if func_req == True:
        self.__browser.close()

    elif isinstance(func_req, list) and func_req[0] == 'screen':
        browser.get_screenshot_as_file("screenshot.png")
        files = {'photo': open('screenshot.png', 'rb')}
        data = {'chat_id': func_req[1]}
        requests.post(f'https://api.telegram.org/bot{api_token}/sendPhoto', files=files, data=data)
    stores_urls = []

    # перебор всех страниц
    for page_num in range(1, 300):
        # открытие страницы
        browser.get(page_url.format(page=page_num))

        # сохранение ссылок на магазины
        urls_from_page = __get_stores_urls_on_page(wait, browser)
        stores_urls += urls_from_page

        # завершение работы при попадании на последнюю страницу
        if len(urls_from_page) != 16:
            break

    return stores_urls


def get_goods_urls(browser, wait, wait_small, url):
    func_req = func_requests_tg_api()
    if func_req == True:
        self.__browser.close()

    elif isinstance(func_req, list) and func_req[0] == 'screen':
        browser.get_screenshot_as_file("screenshot.png")
        files = {'photo': open('screenshot.png', 'rb')}
        data = {'chat_id': func_req[1]}
        requests.post(f'https://api.telegram.org/bot{api_token}/sendPhoto', files=files, data=data)


    goods_urls = []
    # перебор всех страниц
    for page_num in range(1, 50):
        # открытие страницы магазина
        browser.get(url+f'?page={page_num}')

        # сохранение ссылок на магазины
        urls_from_page = __get_goods_urls_on_page(wait, wait_small, browser)
        goods_urls += urls_from_page

        # завершение работы при попадании на последнюю страницу
        if len(urls_from_page) != 18:
            break

    return goods_urls

