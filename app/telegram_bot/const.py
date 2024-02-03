import os

PHONE_NUMBER = os.getenv('PHONE_NUMBER')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
DATABASE_ENCRYPTION_KEY = os.getenv('DATABASE_ENCRYPTION_KEY')
BOT_ID = os.getenv('BOT_ID')
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID_GROUP = os.getenv('CHAT_ID_GROUP')
CHAT_ID_ERRORS = os.getenv('CHAT_ID_ERRORS')

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

max_message_length = 4096
re_smile = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002600-\U000026FF\U00002700-\U000027BF]+'
interest_hashtags = ['#крипто', '#россия', '#стейблкоины', '#бонды']
interesting_word_pattern = [r'\bкрипт\S*\b', 'IPO', r'\bторг\S*\b', r'\bакц\S*\b', r'\bбонд\S*\b', r'\bдивид\S*\b', 'ЦБ']
