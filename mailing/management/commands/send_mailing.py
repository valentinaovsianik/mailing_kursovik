from django.core.management.base import BaseCommand

from mailing.models import Mailing
from mailing.services import process_mailing


class Command(BaseCommand):
    """Отправка рассылки вручную."""

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int, help="ID рассылки")

    def handle(self, *args, **options):
        mailing_id = options["mailing_id"]
        try:
            mailing = Mailing.objects.get(id=mailing_id)
            process_mailing(mailing)
            self.stdout.write(self.style.SUCCESS(f"Рассылка {mailing_id} успешно обработана."))
        except Mailing.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Рассылка с ID {mailing_id} не найдена."))
