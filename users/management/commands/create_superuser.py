from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        email = input("Введите email суперпользователя: ")
        password = input("Введите пароль суперпользователя: ")

        if User.objects.filter(email=email).exists():
            self.stdout.write(f"Суперпользователь с email {email} уже существует.")
        else:
            user = User.objects.create(email=email, is_superuser=True, is_staff=True, is_active=True)
            user.set_password(password)
            user.save()
            self.stdout.write(f"Суперпользователь {email} успешно создан!")
