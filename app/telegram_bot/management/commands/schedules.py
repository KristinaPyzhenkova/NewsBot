import json

from django_celery_beat.models import IntervalSchedule
from django.core.management.base import BaseCommand

from telegram_bot import tasks
from telegram_bot.helpers import get_or_create_then_update_task


def timing_message():
    schedule = IntervalSchedule.objects.get_or_create(every=5, period=IntervalSchedule.MINUTES)[0]
    task_name = f'timing_message_tasks'
    task = get_or_create_then_update_task(
        name=f'{task_name}',
        task=f'telegram_bot.tasks.{tasks.new_message_tasks.__name__}',
        schedule=schedule,
        one_off=False,
        kwargs=json.dumps({'task_name': task_name})
    )


class Command(BaseCommand):
    help = 'Получание и отправка обновлений.'

    def handle(self, *args, **options):
        timing_message()
