import logging

from telegram.constants import ParseMode
from telegram import Update, ext

from telegram_bot import const

logger = logging.getLogger('main')


BOT_TOKEN = const.BOT_TOKEN
application = ext.ApplicationBuilder().token(BOT_TOKEN).build()


async def send_messages(
    summary_message: str, chat_id: int = const.CHAT_ID_GROUP, disable_notification: bool = False
) -> None:
    try:
        await application.bot.send_message(
            text=summary_message,
            chat_id=chat_id,
            disable_notification=disable_notification,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f'{e = }')
        await application.bot.send_message(
            text=summary_message,
            chat_id=chat_id,
            disable_notification=disable_notification,
            disable_web_page_preview=True
        )


async def edit_message(summary_message: str, message_id: int) -> None:
    try:
        await application.bot.edit_message_text(
            text=summary_message,
            chat_id=const.CHAT_ID_GROUP,
            message_id=message_id,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f'{e = }')
        await application.bot.edit_message_text(
            text=summary_message,
            message_id=message_id,
            chat_id=const.CHAT_ID_GROUP,
            disable_web_page_preview=True
        )


def main():
    application.run_polling(allowed_updates=Update.ALL_TYPES)
