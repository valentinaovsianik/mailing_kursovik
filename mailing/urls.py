from django.urls import path
from .views import AboutView, ContactsView
from . import views
from .views import (
    RecipientListView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView, MessageCreateView, MessageListView, MessageUpdateView, MessageDeleteView, MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, MailingAttemptListView
)


app_name = "mailing"

urlpatterns = [
    path('', views.index, name='index'), # Главная страница приложения
    path('about/', AboutView.as_view(), name='about'), # Страница О нас
    path('contacts/', ContactsView.as_view(), name='contacts'), # Страница контактов

    path('recipients/', RecipientListView.as_view(), name='recipient_list'),
    path('recipients/create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/<int:pk>/update/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipients/<int:pk>/delete/', RecipientDeleteView.as_view(), name='recipient_delete'),

    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),

    path('attempts/', MailingAttemptListView.as_view(), name='mailing_attempt_list'),
]
