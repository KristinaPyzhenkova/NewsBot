import logging
import asyncio

from telegram_bot import db, models, aiotdlib_client
from telegram_bot.aiotdlib_helpers import (
    retrieve_messages, retrieve_groups,
    process_messages, get_chat,
    process_chats
)
from telegram_bot.helpers import send_long_msg, handle_exceptions_async

logger = logging.getLogger('main')
BotDB = db.BotDB()


@handle_exceptions_async(log_to_telegram=True, reraise_exception=False)
async def get_updates_handle():
    channels = BotDB.get_channels()
    tg_client = await aiotdlib_client.AiotdlibClient.get_instance()
    chats_list = []
    for channel in channels:
        if channel.type == 'chatFolderInfo':
            groups_in_link = await retrieve_groups(tg_client.bot, channel.folder_url)
            if groups_in_link:
                chat_ids_in_link = groups_in_link['groups']
                chats_coros = [get_chat(tg_client.bot, chat_id=chat_id) for chat_id in chat_ids_in_link]
                chat_folder_chats = await asyncio.gather(*chats_coros)
                chats_list += [dict(elem) for elem in chat_folder_chats if elem is not None]
        elif channel.type == 'chatTypeSupergroup':
            chat_details = await get_chat(tg_client.bot, channel.chat_id)
            chats_list.append(dict(chat_details))
    chats_df = await process_chats(tg_client.bot, chats_list)
    messages_list = []
    for _, chat in chats_df[chats_df['is_supported']].iterrows():
        msg_list = await retrieve_messages(tg_client.bot, chat['chat_id'])
        messages_list += msg_list
        logger.info(f'Current len of messages: {len(messages_list)}')
    check_messages, largest_value_date = await process_messages(messages_list)
    if not len(check_messages):
        return
    for check_message in check_messages['text']:
        await send_long_msg(check_message)
    last_updated_at = models.Setting.objects.get(name='last_updated_at')
    last_updated_at.number = largest_value_date
    last_updated_at.save()
