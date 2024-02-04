from django.contrib import admin

from telegram_bot import models


@admin.register(models.Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'value', 'number',
        'boolean', 'text',
    )
    search_fields = ['name', 'text']


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'channel',
        'media_album_id',
        'date', 'interaction_info',
        'text', 'type',
        'view_count',
        'forward_count', 'reply_count',
        'reactions_info', 'reactions_total_count',
        'message_id', 'is_published'
    )
    search_fields = ['text']
    list_filter = ('is_published',)


@admin.register(models.Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type', 'title',
        'folder_url', 'slug',
        'chat_id', 'supergroup_id',
    )
    search_fields = ['title', 'chat_id']


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name', 'value',
        'exchange', 'modified',
    )
    search_fields = ['name']
