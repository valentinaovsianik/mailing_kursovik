from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from .models import User


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("mailing:index")

    def form_valid(self, form):
        # Создаем пользователя и выполняем авторизацию
        user = form.save()
        login(self.request, user)

        # Отправляем письмо о регистрации
        self.send_registration_email(user)

        return super().form_valid(form)


    def send_registration_email(self, user):
        subject = "Подтверждение регистрации"
        message = f"Здравствуйте, {user.email}!\n\nДобро пожаловать на наш сайт."
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )


class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("mailing:index")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("mailing:index")


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("mailing:index")

    def get_object(self, queryset=None):
        return self.request.user  # Пользователь может изменять только свой профиль


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/profile.html"

    def get_object(self):
        return self.request.user


@login_required
def profile_edit(request):
    user = request.user
    form = UserProfileForm(instance=user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("users:profile")

    return render(request, "users/profile_edit.html", {"form": form})
