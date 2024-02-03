import asyncio
from django.core.management.base import BaseCommand

from telegram_bot.bot import (
    main
)


class Command(BaseCommand):
    help = 'Запуске телеграм-бота.'

    def handle(self, *args, **options):
        asyncio.run(main())
