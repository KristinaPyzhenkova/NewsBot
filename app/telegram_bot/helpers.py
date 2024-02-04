from __future__ import annotations
import logging
import re
from typing import Optional, Union, List, Any
from functools import wraps
import traceback
import requests

from django.urls import reverse
from django.utils.html import format_html
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from bs4 import BeautifulSoup
from tradingview_ta import TA_Handler, Interval, Exchange

from telegram_bot import const, bot

logger = logging.getLogger('main')


def strip_stacktrace(exc: Union[str, Exception]) -> str:
    stacktrace_regex = r"(#[0-9]* 0x.*|Stacktrace:)\n"
    str_without_stacktrace = re.sub(stacktrace_regex, '', str(exc), 0, re.MULTILINE)
    return str_without_stacktrace


async def log_error_with_traceback(e: Exception, log_to_telegram=False) -> None:
    msg = strip_stacktrace(f'{str(e)}\n{traceback.format_exc()}')
    logger.error(msg)
    if log_to_telegram:
        await send_long_msg(msg, chat_id=const.CHAT_ID_ERRORS)


def handle_exceptions_async(log_to_telegram=True, reraise_exception=False):
    def exceptions_decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                await log_error_with_traceback(e, log_to_telegram=log_to_telegram)
                if reraise_exception:
                    raise e
        return wrapper
    return exceptions_decorator


def break_message_into_parts(message_text: str) -> List[str]:
    message_parts = []
    while len(message_text) > const.max_message_length:
        last_newline_idx = message_text.rfind('\n', 0, const.max_message_length)
        if last_newline_idx == -1:
            last_newline_idx = const.max_message_length
        message_parts.append(message_text[:last_newline_idx])
        message_text = message_text[last_newline_idx:]

    message_parts.append(message_text)
    return message_parts


@handle_exceptions_async(log_to_telegram=True, reraise_exception=False)
async def send_long_msg(message: str, chat_id: int = const.CHAT_ID_GROUP) -> None:
    if len(message) <= const.max_message_length:
        await bot.send_messages(message, chat_id=chat_id)
    else:
        message_parts = break_message_into_parts(message)
        for idx, part in enumerate(message_parts, start=1):
            await bot.send_messages(part, chat_id=chat_id)


def retry_logger(retry_state: Any) -> None:
    logger.info(f"Retrying {retry_state.fn}: attempt {retry_state.attempt_number}...")


def check_for_hashtags(text: str) -> bool:
    has_interesting_hashtags = any(re.search(re.escape(hashtag), text) for hashtag in const.interest_hashtags)
    has_interesting_word = any(re.search(pattern, text) for pattern in const.interesting_word_pattern)
    if has_interesting_hashtags or has_interesting_word:
        return True
    return False


def remove_hashtags_and_smileys(text: str) -> str:
    text_without_hashtags = re.sub(r'#\w+', '', text)
    text_without_smileys = re.sub(
        const.re_smile,
        '',
        text_without_hashtags
    )
    text_without_smileys = re.sub(r'️', ' ', text_without_smileys)
    return text_without_smileys.strip()


def short_text(attribute, url_attr_name=None):
    def short_text_(self, obj):
        text_value = getattr(obj, attribute)
        if text_value and len(text_value) > 50:
            return text_value[:50] + '...'
        else:
            return text_value

    short_text_.short_description = url_attr_name or attribute
    return short_text_


def model_link(model, model_name=None, admin_name=None, reverse_name=None):
    model_field_name = model_name or model.__name__.lower()
    admin_name = admin_name or getattr(model._meta, 'verbose_name', None) or model_field_name
    reverse_name = reverse_name or model_field_name

    def model_link_(self, obj):
        foreign_model = getattr(obj, model_field_name)
        if foreign_model:
            url = reverse(
                f'admin:{foreign_model._meta.app_label}_{reverse_name}_change',
                args=[getattr(foreign_model, foreign_model._meta.pk.name)],
            )
            return format_html(f"<a href='{url}'>{foreign_model}</a>")

    model_link_.admin_order_field = model_field_name
    model_link_.short_description = admin_name

    return model_link_


def get_or_create_then_update_task(
    name: str,
    task: str,
    schedule: Optional[IntervalSchedule] = None,
    one_off: bool = False,
    kwargs: Optional[str] = None
) -> PeriodicTask:
    periodic_task = PeriodicTask.objects.filter(name=name).first()
    if periodic_task:
        periodic_task.interval = str(schedule)
        periodic_task.task = task
        periodic_task.one_off = one_off
        periodic_task.kwargs = kwargs or '{}'
        periodic_task.save()
    else:
        periodic_task, _ = PeriodicTask.objects.get_or_create(
            interval=schedule,
            name=name,
            task=task,
            one_off=one_off,
            kwargs=kwargs or '{}',
        )

    return periodic_task


def get_currency_rate(cur: str) -> float:
    url = const.url_currency.format(cur)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    result = soup.find("div", class_="BNeawe iBp4i AP7Wnd").get_text().split()
    return float(result[0].replace(",", "."))


def get_crypto_currency_rate(cur: str) -> float:
    tesla = TA_Handler(
        symbol=f"{cur}USDT",
        screener="Crypto",
        exchange="Binance",
        interval=Interval.INTERVAL_5_MINUTES
    )
    return tesla.get_analysis().indicators['close']
