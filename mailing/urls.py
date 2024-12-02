from django.urls import path
from .views import AboutView, ContactsView
from . import views

app_name = "mailing"

urlpatterns = [
    path('', views.index, name='index'), # Главная страница приложения
    path('about/', AboutView.as_view(), name='about'), # Страница О нас
    path('contacts/', ContactsView.as_view(), name='contacts'), # Страница контактов
]
