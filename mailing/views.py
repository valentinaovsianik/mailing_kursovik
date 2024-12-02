from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Recipient, Message, Mailing, MailingAttempt
from .forms import RecipientForm, MessageForm, MailingForm, MailingAttemptForm

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


# Представления для модели Recipient
class RecipientListView(ListView):
    model = Recipient
    template_name = 'mailing/recipient_list.html'
    context_object_name = 'recipients'

class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('recipient_list')

class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('recipient_list')

class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'mailing/recipient_confirm_delete.html'
    success_url = reverse_lazy('recipient_list')

# Представления для модели Message
class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'

class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('message_list')

class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('message_list')

class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('message_list')

# Представления для модели Mailing
class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'

class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing_list')

class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing_list')

class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_list')

# Представления для модели MailingAttempt
class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = 'mailing/mailing_attempt_list.html'
    context_object_name = 'attempts'

