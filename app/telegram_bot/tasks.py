import logging
import requests

from celery.contrib.abortable import AbortableTask

from app.celery import app

logger = logging.getLogger('main')


@app.task(bind=True, max_retries=None, base=AbortableTask)
def new_message_tasks(self, task_name: str = None) -> None:
    try:
        logger.info(f'{task_name = }')
        _ = requests.get('http://web:8000/get_news/')
    except Exception as e:
        logger.error(f'{e = }')


@app.task(bind=True, max_retries=None, base=AbortableTask)
def new_currency_tasks(self, task_name: str = None) -> None:
    try:
        logger.info(f'{task_name = }')
        _ = requests.get('http://web:8000/get_currency/')
    except Exception as e:
        logger.error(f'{e = }')
