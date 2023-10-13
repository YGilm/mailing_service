from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views import View
from django.views.generic.edit import CreateView
from .models import User
from .forms import UserRegisterForm
from . import services


class RegisterView(CreateView):
    """
    Класс-контроллер для отображения страницы регистрации нового пользователя.
    """

    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)

            url = reverse('users:email_verification', args=[self.object.email_verification_code])
            absolute_url = self.request.build_absolute_uri(url)

            services.send_verification(email=self.object.email, url=absolute_url)

            messages.success(self.request, 'Ссылка для верификации отправлена на вашу электронную почту!')
            self.object.save()

        return super().form_valid(form)


class EmailVerificationView(View):
    def get(self, request, email_verification_code):
        try:
            user = User.objects.get(email_verification_code=email_verification_code)
            user.email_verified = True
            user.save()
            messages.success(request, 'Ваша почта успешно подтверждена!')
        except User.DoesNotExist:
            messages.error(request, 'Неверная или устаревшая ссылка подтверждения.')

        return redirect('users:login')
