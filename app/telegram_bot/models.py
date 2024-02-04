import logging

from django.db import models


logger = logging.getLogger('main')


class CommonFields(models.Model):
    """Common fields across models."""
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения')

    class Meta:
        abstract = True


class Setting(CommonFields):
    name = models.CharField(max_length=100, primary_key=True)
    value = models.TextField(null=True, blank=True, max_length=250)
    number = models.IntegerField(null=True, blank=True)
    boolean = models.IntegerField(default=True)
    text = models.TextField(blank=True)


class Channel(CommonFields):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(
        max_length=250,
        verbose_name='type',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='title',
    )
    folder_url = models.CharField(
        max_length=250,
        verbose_name='folder_url',
        null=True,
        blank=True
    )
    slug = models.CharField(
        max_length=250,
        verbose_name='slug',
        null=True,
        blank=True
    )
    chat_id = models.CharField(
        max_length=250,
        null=True,
        blank=True
    )
    supergroup_id = models.CharField(
        max_length=250,
        verbose_name='supergroup_id',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Каналы'


class Message(CommonFields):
    id = models.BigAutoField(primary_key=True)
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        verbose_name='Канал',
    )
    media_album_id = models.CharField(
        max_length=50,
    )
    date = models.CharField(
        max_length=50,
    )
    interaction_info = models.TextField()
    text = models.TextField()
    type = models.CharField(
        max_length=50,
        verbose_name='type',
    )
    view_count = models.PositiveIntegerField(
        default=0
    )
    forward_count = models.PositiveIntegerField(
        default=0
    )
    reply_count = models.PositiveIntegerField(
        default=0
    )
    reactions_info = models.TextField()
    reactions_total_count = models.PositiveIntegerField(
        default=0
    )
    message_id = models.CharField(
        max_length=50,
    )
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.message_id}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Currency(CommonFields):
    USD = 'доллар'
    CNY = 'юань'
    EUR = 'евро'
    BTC = 'BTC'
    ETH = 'ETH'
    CURRENCY_NAME = (
        (USD, USD),
        (EUR, EUR),
        (CNY, CNY),
        (BTC, BTC),
        (ETH, ETH),
    )
    CUR = 'currency'
    CRYPTO = 'crypto'
    EXCHANGE = (
        (CUR, CUR),
        (CRYPTO, CRYPTO),
    )
    name = models.CharField(choices=CURRENCY_NAME, default=USD, max_length=12, null=True, blank=True)
    value = models.FloatField(null=True, blank=True)
    exchange = models.CharField(choices=EXCHANGE, default=CUR, max_length=12, null=True, blank=True)
