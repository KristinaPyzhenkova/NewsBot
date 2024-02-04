from __future__ import annotations
import os
import logging
from typing import Dict, Any, Tuple

from django.db.models.query import QuerySet

from telegram_bot import models

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
logger = logging.getLogger('main')


class BotDB:

    @staticmethod
    def get_channels() -> QuerySet[models.Channel]:
        """Получаем каналы."""
        try:
            channels = models.Channel.objects.all()
            return channels
        except Exception as e:
            logger.error(f'{e}')

    @staticmethod
    def get_channel(chat_id: int) -> models.Channel:
        """Получаем канал."""
        try:
            channel = models.Channel.objects.filter(chat_id=chat_id).first()
            return channel
        except Exception as e:
            logger.error(f'{e}')

    @staticmethod
    def update_or_create_channel(data: Dict[str, int]) -> models.Channel:
        """Добавляем канал."""
        try:
            defaults = {
                'title': data.get('title'),
                'folder_url': data.get('folder_url', None),
                'type': data.get('type', None),
                'slug': data.get('slug', None),
                'supergroup_id': data.get('supergroup_id', None)
            }
            channel, created = models.Channel.objects.update_or_create(
                chat_id=data['chat_id'],
                defaults=defaults
            )
            return channel
        except Exception as e:
            logger.error(f'{e = }')

    @staticmethod
    def update_or_create_list(data: Dict[str, int, Any]) -> models.Channel:
        """Добавляем список каналов."""
        try:
            defaults = {
                'title': data.get('title'),
                'chat_id': data.get('chat_id', None),
                'type': data.get('type', None),
                'slug': data.get('slug', None),
                'supergroup_id': data.get('supergroup_id', None)
            }
            channel, created = models.Channel.objects.update_or_create(
                folder_url=data['folder_url'],
                defaults=defaults
            )
            return channel
        except Exception as e:
            logger.error(f'{e = }')

    @staticmethod
    def update_or_create_message(
        message_id: int, defaults: Dict[str, int, Any]
    ) -> Tuple[models.Channel, bool]:
        """Получаем существующее или создаем новое сообщение."""
        try:
            updated_message, created = models.Message.objects.update_or_create(
                message_id=message_id,
                defaults=defaults
            )
            return updated_message, created
        except Exception as e:
            logger.error(f'{e}')

    @staticmethod
    def get_currencies() -> QuerySet[models.Currency]:
        """Получаем валюты."""
        try:
            currencies = models.Currency.objects.all()
            return currencies
        except Exception as e:
            logger.error(f'{e}')
