from loguru import logger
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions

from parser.utilities import xpaths, image_utils
from parser.utilities.system_config import page_url


def get_reviews(browser, wait, small_wait, url):
    # открытие страницы с отзывами
    browser.get(url)

    reviews = []

    # перебор всех отзывов
    for review_num in range(1, 6):
        # проверка на существование отзыва
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.review.format(review_num=(review_num + 5)))))
        except exceptions.TimeoutException:
            return reviews

        review = dict()

        try:
            review['name'] = small_wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.review_name.format(review_num=(review_num + 5))))).text
        except:
            review['name'] = None

        try:
            review['text'] = small_wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.review_text.format(review_num=(review_num + 5))))).text
        except:
            review['text'] = None

        try:
            review['rating'] = small_wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.review_rating.format(review_num=(review_num + 5))))).get_attribute('innerHTML').split('style="--rating: ')[1].split('"')[0]
        except:
            review['rating'] = None

        try:
            review['purchase'] = small_wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.review_purchase.format(review_num=(review_num + 5))))).text.split('Покупок:\n')[1].split('\n')[0]
        except:
            review['purchase'] = None

        try:
            review['location'] = small_wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.review_location.format(review_num=(review_num + 5))))).text
        except:
            review['location'] = None

        try:
            review['date'] = small_wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.review_date.format(review_num=(review_num + 5))))).text
        except:
            review['date'] = None

        try:
            review['answer'] = small_wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.review_answer.format(review_num=(review_num + 5))))).text
        except:
            review['answer'] = None

        try:
            avatar = small_wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.review_img.format(review_num=(review_num + 5))))).get_attribute('src')
            if not avatar:
                review['img'] = None
            elif avatar.split('/')[-1].split('.')[0] != 'no-img':
                image_utils.download_image(avatar, 'icons', avatar.split('/')[-1].split('.')[0])
                review['img'] = avatar.split('/')[-1]
            else:
                review['img'] = None
        except:
            review['img'] = None

        reviews.append(review)

    return reviews
