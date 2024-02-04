import asyncio
import logging

from django.http import HttpResponse

from telegram_bot.user_bot import get_updates_handle, get_currency_handle

logger = logging.getLogger('main')
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def get_news_view(request):
    loop.run_until_complete(get_updates_handle())
    return HttpResponse("get_updates_handle выполнена успешно!")


def get_currency_view(request):
    loop.run_until_complete(get_currency_handle())
    return HttpResponse("get_currency_view выполнена успешно!")
