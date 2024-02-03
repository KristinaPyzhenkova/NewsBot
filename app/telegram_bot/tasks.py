import logging
import requests

from requests.auth import HTTPBasicAuth
from celery.contrib.abortable import AbortableTask

from app.celery import app
from telegram_bot import const

logger = logging.getLogger('main')


@app.task(bind=True, max_retries=None, base=AbortableTask)
def new_message_tasks(self, task_name: str = None) -> None:
    try:
        logger.info(f'{task_name = }')
        # response = requests.post('http://web:8000/get_news/', auth=HTTPBasicAuth(const.username, const.password))
        # logger.info(f'{task_name = }')
        _ = requests.get('http://web:8000/get_news/')
    except Exception as e:
        logger.error(f'{e = }')
