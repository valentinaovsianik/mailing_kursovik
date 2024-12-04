from django.views.generic import View, DetailView, TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from .models import Recipient, Message, Mailing, MailingAttempt
from .forms import RecipientForm, MessageForm, MailingForm, MailingAttemptForm
from mailing.services import process_mailing
from django.http import HttpResponseRedirect
from django.contrib import messages


class ManagerRequiredMixin(UserPassesTestMixin):
    """Миксин для проверки прав менеджера"""
    def test_func(self):
        return self.request.user.groups.filter(name='Менеджер').exists()

class OwnerOrManagerMixin(UserPassesTestMixin):
    """Миксин для проверки доступа к объекту (владелец или менеджер)"""
    def test_func(self):
        obj = self.get_object()
        is_manager = self.request.user.groups.filter(name='Менеджер').exists()
        is_owner = obj.owner == self.request.user
        return is_manager or is_owner


class AboutView(TemplateView):
    template_name = 'mailing/about.html'


class ContactsView(TemplateView):
    template_name = 'mailing/contacts.html'


def index(request):
    """Статистика по всем рассылкам сервиса на главной странице"""
    #Подсчёт количества всех рассылок
    total_mailings = Mailing.objects.count()

    # Подсчёт количества активных рассылок (со статусом 'Запущена')
    active_mailings = Mailing.objects.filter(status='started').count()

    #Подсчёт количества уникальных получателей
    unique_recipients = Recipient.objects.distinct().count()
    #
    context = {
         'total_mailings': total_mailings,
         'active_mailings': active_mailings,
         'unique_recipients': unique_recipients,
     }
    return render(request, 'mailing/index.html', context)


# Представления для модели Recipient
class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = 'mailing/recipient_detail.html'
    context_object_name = 'recipient'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджер').exists():
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='Менеджер').exists()
        return context


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = 'mailing/recipient_list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджер').exists():
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='Менеджер').exists()
        return context


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='Менеджер').exists()
        return context

class RecipientUpdateView(LoginRequiredMixin, OwnerOrManagerMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='Менеджер').exists()
        return context

class RecipientDeleteView(LoginRequiredMixin, OwnerOrManagerMixin, DeleteView):
    model = Recipient
    template_name = 'mailing/recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing:recipient_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='Менеджер').exists()
        return context

# Представления для модели Message
class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджер').exists():
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='Менеджер').exists()
        return context


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджер').exists():
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='Менеджер').exists()
        return context


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='Менеджер').exists()
        return context

class MessageUpdateView(LoginRequiredMixin, OwnerOrManagerMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='Менеджер').exists()
        return context

class MessageDeleteView(LoginRequiredMixin, OwnerOrManagerMixin, DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('message_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='Менеджер').exists()
        return context


# Представления для модели Mailing
class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджер').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='Менеджер').exists()

        mailing = self.object
        attempts = MailingAttempt.objects.filter(mailing=mailing)
        context['attempts'] = attempts
        context['successful_attempts'] = attempts.filter(status='success').count()  # Подсчет успешных попыток
        context['failed_attempts'] = attempts.filter(status='failure').count()  # Подсчет неудачных попыток
        context['total_messages_sent'] = attempts.count()  # Общее количество попыток рассылки

        return context


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджер').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='Менеджер').exists()
        return context

class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='Менеджер').exists()
        return context

class MailingUpdateView(LoginRequiredMixin, OwnerOrManagerMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='Менеджер').exists()
        return context

class MailingDeleteView(LoginRequiredMixin, OwnerOrManagerMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='Менеджер').exists()
        return context


class MailingSendView(LoginRequiredMixin, View):
    """Ручной запуск рассылки"""
    def post(self, request, pk, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=pk)
        if not (mailing.owner == request.user or request.user.groups.filter(name='Менеджер').exists()):
            return JsonResponse({"success": False, "message": "У вас нет доступа к запуску этой рассылки."})
        try:
            process_mailing(mailing)
            messages.success(request, "Рассылка успешно запущена.")
        except Exception as e:
            messages.error(request, f"Ошибка при запуске рассылки: {str(e)}")

        return HttpResponseRedirect(reverse('mailing:mailing_list'))


# Представления для модели MailingAttempt
class MailingAttemptListView(LoginRequiredMixin, ManagerRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'mailing/mailing_attempt_list.html'
    context_object_name = 'attempts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['is_manager'] = user.groups.filter(name='Менеджер').exists()
        context['is_creator'] = user.groups.filter(name='Пользователь-создатель').exists()

        return context

    def get_queryset(self):
        user = self.request.user
        queryset = MailingAttempt.objects.filter(mailing__owner=user)

        mailing_id = self.kwargs.get('mailing_id')
        if mailing_id:
            queryset = queryset.filter(mailing_id=mailing_id)

        return queryset