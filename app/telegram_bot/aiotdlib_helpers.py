from __future__ import annotations
import logging
from typing import List, Any, Tuple, Dict
from tenacity import retry, stop_after_attempt, retry_if_result, wait_fixed
import asyncio

import pandas as pd
from aiotdlib.api import types
from aiotdlib import Client

from telegram_bot.helpers import (
    handle_exceptions_async,
    retry_logger,
    check_for_hashtags,
    remove_hashtags_and_smileys
)
from telegram_bot.db import BotDB
from telegram_bot import const, models

logger = logging.getLogger('main')


@handle_exceptions_async(log_to_telegram=True, reraise_exception=False)
async def update_messages_list(
    response: Any,
    messages_list: List[Any],
    total_messages: int,
    receive: bool,
    receive_limit: int = 15
) -> Tuple[bool, int, List[Dict[str, int, Any]]]:
    for message in response.messages:
        if message.content.ID == 'messageText':
            message_extracted = {
                'message_id': message.id,
                'chat_id': message.chat_id,
                'date': message.date,
                'interaction_info': dict(message.interaction_info) if message.interaction_info else None,
                'text': message.content.text.text,
                'type': 'messageText'
            }
            messages_list.append(message_extracted)
        elif message.content.ID == 'messagePhoto':
            message_extracted = {
                'message_id': message.id,
                'chat_id': message.chat_id,
                'date': message.date,
                'interaction_info': dict(message.interaction_info) if message.interaction_info else None,
                'text': message.content.caption.text,
                'media_album_id': message.media_album_id,
                'type': 'messagePhoto'
            }
            messages_list.append(message_extracted)
        # from_message_id = message.id
        total_messages += 1

    if total_messages > receive_limit or not response.total_count:
        receive = False
    return receive, total_messages, messages_list


@handle_exceptions_async(log_to_telegram=False, reraise_exception=False)
async def get_history(tg: Client, chat_id: int, from_message_id: int = 0) -> Any:
    return await tg.api.get_chat_history(
        chat_id=chat_id,
        limit=10,
        from_message_id=from_message_id,
        offset=0,
        only_local=False
    )


@handle_exceptions_async(log_to_telegram=True, reraise_exception=False)
async def retrieve_messages(tg: Client, chat_id: int) -> List[Dict[str, int, Any]]:
    receive = True
    messages_list = []
    total_messages = 0
    while receive:
        response = await get_history(tg, chat_id)
        if response:
            receive, total_messages, messages_list = await update_messages_list(
                response, messages_list, total_messages, receive
            )
    return messages_list


@handle_exceptions_async(log_to_telegram=True, reraise_exception=False)
async def retrieve_groups(tg: Client, invite_link: str) -> Dict[str, int, List[int]]:
    result = await tg.api.check_chat_folder_invite_link(invite_link)
    return {
        'folder_url': invite_link,
        'title': result.chat_folder_info.title,
        'type': result.chat_folder_info.ID,
        'groups': result.missing_chat_ids
    }


@handle_exceptions_async(log_to_telegram=True, reraise_exception=False)
async def get_message_link(tg: Client, chat_id: int, message_id: int) -> str:
    result = await tg.api.get_message_link(chat_id, message_id)
    return result.link


@handle_exceptions_async(log_to_telegram=True, reraise_exception=False)
async def search_public_chat(tg: Client, username: str) -> Dict[str, int]:
    result = await tg.api.search_public_chat(username)
    if result.type_.ID == 'chatTypeSupergroup':
        # получение bot_id
        # user_info = await telegram.api.get_me()
        # bot_id = user_info.id
        member_id = types.MessageSenderUser(user_id=const.BOT_ID)
        get_chat_member = await tg.api.get_chat_member(
            chat_id=result.id,
            member_id=member_id
        )
        if get_chat_member.joined_chat_date == 0:
            await tg.api.join_chat(result.id)
        return {
            'chat_id': result.id,
            'title': result.title,
            'type': result.type_.ID,
            'slug': username,
            'supergroup_id': result.type_.supergroup_id
        }


@handle_exceptions_async(log_to_telegram=True, reraise_exception=False)
@retry(stop=stop_after_attempt(5),
       retry=retry_if_result(lambda result: result is None),
       wait=wait_fixed(3),
       before=retry_logger)
async def get_chat(tg: Client, chat_id: int) -> Any:
    result = await tg.api.get_chat(chat_id)
    return result


@handle_exceptions_async(log_to_telegram=True, reraise_exception=False)
async def process_interaction_info(messages: pd.DataFrame) -> pd.DataFrame:
    messages['interaction_info'].fillna(0, inplace=True)
    messages['view_count'] = messages['interaction_info'].apply(
        lambda x: x.get('view_count') if x != 0 and isinstance(x, dict) else 0)
    messages['forward_count'] = (messages['interaction_info'].apply(
        lambda x: x['forward_count'] if x != 0 else 0)
    )
    messages['reply_count'] = (messages['interaction_info'].apply(
        lambda x: dict(x['reply_info'])['reply_count'] if x != 0 and x['reply_info'] else 0)
    )
    messages['reactions_info'] = messages['interaction_info'].apply(lambda x: x['reactions'] if x != 0 else 0)
    messages['reactions_total_count'] = messages['reactions_info'].apply(
        lambda x: sum(_.total_count for _ in x) if x != 0 else 0)
    return messages


@handle_exceptions_async(log_to_telegram=True, reraise_exception=False)
async def process_messages(messages_list: List[Dict[str, int, Any]]) -> Tuple[pd.DataFrame, int]:
    messages = pd.DataFrame.from_dict(messages_list)
    messages = messages.dropna(subset=['text']).copy()
    messages = messages[messages['text'] != ''].copy()
    messages = messages.groupby(['chat_id', 'date']).last().reset_index()
    last_updated_at = models.Setting.objects.get_or_create(name='last_updated_at')[0]
    messages = messages[messages['date'] > last_updated_at.number].copy()
    messages = await process_interaction_info(messages)
    updated_messages = []
    if len(messages):
        for index, row in messages.iterrows():
            if check_for_hashtags(row['text']):
                text = remove_hashtags_and_smileys(row['text'])
                if not len(text):
                    continue
                defaults = {
                    'channel': BotDB.get_channel(row['chat_id']),
                    'media_album_id': str(row.get('media_album_id', None)),
                    'date': str(row['date']),
                    'interaction_info': row['interaction_info'],
                    'text': text,
                    'type': row['type'],
                    'forward_count': row['forward_count'],
                    'reply_count': row['reply_count'],
                    'reactions_info': row['reactions_info'],
                    'reactions_total_count': row['reactions_total_count'],
                }
                updated_message, created = BotDB.update_or_create_message(row['message_id'], defaults)
                if created or updated_message:
                    updated_messages.append(text)
    updated_messages_df = pd.DataFrame({'text': updated_messages})
    return updated_messages_df, messages['date'].max()


async def process_chats(tg: Client, chats_list: List[Dict[str, int, Any]], max_retries: int = 3) -> pd.DataFrame:
    try:
        chats_df = pd.DataFrame.from_dict(chats_list)
        chats_df['chat_id'] = chats_df['id']
        chats_df['supergroup_id'] = chats_df['type_'].apply(
            lambda x: x.supergroup_id if x.ID == 'chatTypeSupergroup' else None)
        chats_df['supergroup_info'] = None
        for _, chat in chats_df.iterrows():
            if chat['supergroup_id']:
                supergroup_info = await tg.api.get_supergroup(chat['supergroup_id'])
                chats_df.loc[_, 'supergroup_info'] = supergroup_info.status.ID
        chats_df['is_channel'] = chats_df['type_'].apply(lambda x: x.is_channel)
        chats_df['is_supported'] = (chats_df['supergroup_info'].isin(
            ['chatMemberStatusMember', 'chatMemberStatusLeft'])
        )
        chats_df = chats_df[['chat_id', 'title', 'supergroup_id', 'is_channel', 'is_supported', 'supergroup_info']]
        return chats_df
    except TimeoutError as e:
        if max_retries > 0:
            await asyncio.sleep(5)  # Ждем некоторое время перед повторной попыткой
            return await process_chats(tg, chats_list, max_retries - 1)
        else:
            logger.error('Max retries exceeded, giving up.')
    except Exception as e:
        logger.error(f'{e = }')


@handle_exceptions_async(log_to_telegram=True, reraise_exception=False)
async def authorization() -> List[Dict[str, int, Any]]:
    tg = Client(
        api_id=const.API_ID,
        api_hash=const.API_HASH,
        phone_number=const.PHONE_NUMBER,
        database_encryption_key=const.DATABASE_ENCRYPTION_KEY,
        use_message_database=False
    )
    async with tg:
        await tg.api.get_me()
        chats_list = []
        await search_public_chat(tg, 'minaevlife')
        chat_details = await get_chat(tg, -1001297869576)
        chats_list.append(dict(chat_details))
        return chats_list


@handle_exceptions_async(log_to_telegram=True, reraise_exception=False)
async def add_subscription(text: str) -> None:
    tg = Client(
        api_id=const.API_ID,
        api_hash=const.API_HASH,
        phone_number=const.PHONE_NUMBER,
        database_encryption_key=const.DATABASE_ENCRYPTION_KEY,
        use_message_database=False
    )
    async with tg:
        if '/addlist' in text:
            result = await retrieve_groups(tg, text)
            _ = BotDB.update_or_create_list(result)
            return
        elif 't.me' in text:
            username = text.split('/')[-1]
            result = await search_public_chat(tg, username)
        else:
            result = await search_public_chat(tg, text)
        _ = BotDB.update_or_create_channel(result)

