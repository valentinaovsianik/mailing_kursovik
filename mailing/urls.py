from django.urls import path
from .views import AboutView, ContactsView
from . import views
from .views import (
    RecipientDetailView, RecipientListView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView, MailingDetailView, MessageDetailView, MessageCreateView, MessageListView, MessageUpdateView, MessageDeleteView, MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, MailingAttemptListView, MailingSendView,
)


app_name = "mailing"

urlpatterns = [
    path('', views.index, name='index'), # Главная страница приложения
    path('about/', AboutView.as_view(), name='about'), # Страница О нас
    path('contacts/', ContactsView.as_view(), name='contacts'), # Страница контактов

    path('recipients/', RecipientListView.as_view(), name='recipient_list'),
    path('recipients/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipients/create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/<int:pk>/update/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipients/<int:pk>/delete/', RecipientDeleteView.as_view(), name='recipient_delete'),

    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing/<int:pk>/send/', MailingSendView.as_view(), name='mailing_send'),

    path('attempts/', MailingAttemptListView.as_view(), name='mailing_attempt_list'),
]
