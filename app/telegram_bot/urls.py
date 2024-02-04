from django.urls import path
from telegram_bot.views import get_news_view, get_currency_view

urlpatterns = [
    path('get_news/', get_news_view, name='get_news'),
    path('get_currency/', get_currency_view, name='get_currency'),
]
