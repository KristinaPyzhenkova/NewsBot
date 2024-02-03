import logging

from aiotdlib import Client

from telegram_bot import const

logger = logging.getLogger('main')


class AiotdlibClient:
    _instance = None
    created = False

    def __init__(
        self,
        api_id,
        api_hash,
        phone_number,
        database_encryption_key,
        use_message_database,
    ):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.database_encryption_key = database_encryption_key
        self.use_message_database = use_message_database
        self.no_received_times = 0
        self.need_restart = 0
        self.killed = False
        self.bot = None

    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls(
                api_id=const.API_ID,
                api_hash=const.API_HASH,
                phone_number=const.PHONE_NUMBER,
                database_encryption_key=const.DATABASE_ENCRYPTION_KEY,
                use_message_database=False
            )
            cls.created = True
            await cls._instance.run()

        return cls._instance

    async def run(self):
        if self.bot is None:
            self.bot = Client(
                api_id=self.api_id,
                api_hash=self.api_hash,
                phone_number=self.phone_number,
                database_encryption_key=self.database_encryption_key,
                use_message_database=self.use_message_database
            )
            await self.bot.start()

    async def re_run(self):
        if self.bot is not None:
            await self.bot.stop()
        self.bot = Client(
            api_id=self.api_id,
            api_hash=self.api_hash,
            phone_number=self.phone_number,
            database_encryption_key=self.database_encryption_key,
            use_message_database=self.use_message_database
        )
        await self.bot.start()

    def kill(self):
        self.killed = True

    def __str__(self):
        return f"<AiotdlibClient {self.api_id}> "
