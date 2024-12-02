from django.views.generic import TemplateView
from django.shortcuts import render

class AboutView(TemplateView):
    template_name = 'mailing/about.html'


class ContactsView(TemplateView):
    template_name = 'mailing/contacts.html'


def index(request):
    context = {
        'message': 'Здесь будет статистика'
    }
    # # Подсчёт количества всех рассылок
    # total_mailings = Mailing.objects.count()
    #
    # # Подсчёт количества активных рассылок (со статусом 'Запущена')
    # active_mailings = Mailing.objects.filter(status='started').count()
    #
    # # Подсчёт количества уникальных получателей
    # unique_recipients = Recipient.objects.distinct().count()
    #
    # context = {
    #     'total_mailings': total_mailings,
    #     'active_mailings': active_mailings,
    #     'unique_recipients': unique_recipients,
    # }
    return render(request, 'mailing/index.html', context)

