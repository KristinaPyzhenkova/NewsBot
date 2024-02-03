from django.urls import path
from telegram_bot.views import get_news_view

urlpatterns = [
    path('get_news/', get_news_view, name='get_news'),
]
x