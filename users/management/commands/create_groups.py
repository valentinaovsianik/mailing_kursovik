from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mailing.models import Recipient, Message, Mailing
from users.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Создание группы Пользователь
        user_group, created = Group.objects.get_or_create(name="Пользователь")
        if created:
            self.stdout.write(self.style.SUCCESS("Группа 'Пользователь' создана."))

        # Назначение разрешений для Пользователя
        user_permissions = [
            Permission.objects.get(codename="add_mailing", content_type__app_label="mailing"),
            Permission.objects.get(codename="change_mailing", content_type__app_label="mailing"),
            Permission.objects.get(codename="delete_mailing", content_type__app_label="mailing"),
            Permission.objects.get(codename="view_mailing", content_type__app_label="mailing"),
            Permission.objects.get(codename="add_recipient", content_type__app_label="mailing"),
            Permission.objects.get(codename="change_recipient", content_type__app_label="mailing"),
            Permission.objects.get(codename="delete_recipient", content_type__app_label="mailing"),
            Permission.objects.get(codename="view_recipient", content_type__app_label="mailing"),
            Permission.objects.get(codename="view_mailingattempt", content_type__app_label="mailing"),
        ]
        user_group.permissions.set(user_permissions)
        user_group.save()
        self.stdout.write(self.style.SUCCESS("Разрешения для группы 'Пользователь' назначены."))

        # Создание группы Менеджер
        manager_group, created = Group.objects.get_or_create(name="Менеджер")
        if created:
            self.stdout.write(self.style.SUCCESS("Группа 'Менеджер' создана."))

        # Назначение разрешений для Менеджера
        manager_permissions = [
            Permission.objects.get(codename="view_recipient", content_type=ContentType.objects.get_for_model(Recipient)),
            Permission.objects.get(codename="view_mailing", content_type=ContentType.objects.get_for_model(Mailing)),
            Permission.objects.get(codename="view_user", content_type=ContentType.objects.get_for_model(User)),
            Permission.objects.get(codename="change_user", content_type=ContentType.objects.get_for_model(User)),
            Permission.objects.get(codename="change_mailing", content_type=ContentType.objects.get_for_model(Mailing)),
        ]
        manager_group.permissions.set(manager_permissions)
        manager_group.save()
        self.stdout.write(self.style.SUCCESS("Разрешения для группы 'Менеджер' назначены."))

        self.stdout.write(self.style.SUCCESS("Группы и разрешения успешно созданы!"))
