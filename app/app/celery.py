import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'add-every-300-seconds': {
        'task': 'telegram_bot.tasks.new_currency_tasks',
        'schedule': 300.0,
        'kwargs': {'task_name': 'new_currency_tasks'}
    },
}
app.conf.timezone = 'Europe/Moscow'


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
