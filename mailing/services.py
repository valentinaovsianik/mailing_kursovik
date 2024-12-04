from django.core.mail import send_mail
from .models import MailingAttempt
from django.utils.timezone import now
from django.conf import settings


def process_mailing(mailing):
    """Обрабатывает отправку сообщений для указанной рассылки."""
    recipients = mailing.recipients.all()
    message = mailing.message

    for recipient in recipients:
        try:
            # Отправка письма
            send_mail(
                subject=mailing.message.subject,
                message=message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            # Успешная попытка
            MailingAttempt.objects.create(
                mailing=mailing,
                timestamp=now(),
                status='success',
                server_response="Сообщение успешно отправлено.",
            )
        except Exception as e:
            # Неуспешная попытка
            MailingAttempt.objects.create(
                mailing=mailing,
                timestamp=now(),
                status='failed',
                server_response=str(e),
            )
    # Обновляем статус рассылки
    mailing.update_status()
