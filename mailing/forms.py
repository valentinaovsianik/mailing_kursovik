from django import forms

from .models import Mailing, MailingAttempt, Message, Recipient


# Форма для модели Recipient
class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ["email", "full_name", "comment"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите email",
                    "aria-label": "Email",
                }
            ),
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите полное имя",
                    "aria-label": "Full Name",
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control textarea-custom",
                    "placeholder": "Введите комментарий",
                    "rows": 4,
                    "aria-label": "Comment",
                }
            ),
        }


# Форма для модели Message
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]
        widgets = {
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите тему сообщения",
                    "aria-label": "Subject",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "form-control textarea-custom",
                    "placeholder": "Введите текст сообщения",
                    "rows": 6,
                    "aria-label": "Body",
                }
            ),
        }


# Форма для модели Mailing
class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["send_time_start", "send_time_end", "status", "message", "recipients"]

        widgets = {
            "send_time_start": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                    "placeholder": "Выберите начало времени отправки",
                    "aria-label": "Start Time",
                }
            ),
            "send_time_end": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                    "placeholder": "Выберите конец времени отправки",
                    "aria-label": "End Time",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-select",
                    "aria-label": "Status",
                }
            ),
            "message": forms.Select(
                attrs={
                    "class": "form-select",
                    "aria-label": "Message",
                }
            ),
            "recipients": forms.SelectMultiple(
                attrs={
                    "class": "form-control",
                    "size": 5,
                    "aria-label": "Recipients",
                }
            ),
        }


# Форма для модели MailingAttempt
class MailingAttemptForm(forms.ModelForm):
    class Meta:
        model = MailingAttempt
        fields = ["status", "server_response"]
        widgets = {
            "server_response": forms.Textarea(attrs={"rows": 4}),
        }
