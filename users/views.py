from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model, authenticate, login
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views import View
from django.views.generic.edit import CreateView
from .models import User
from .forms import UserRegisterForm, BlockUserForm
from . import services


class ManagerMixin:
    """
    Mixin для определения, является ли пользователь менеджером и ограничения доступа.
    """

    def is_manager(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='Managers').exists()

    def dispatch(self, request, *args, **kwargs):
        if not self.is_manager():
            return HttpResponseForbidden("У вас нет прав доступа к этой странице.")
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        if not form.get_user().email_verified:
            messages.error(self.request, 'Пожалуйста, подтвердите свою электронную почту перед входом.')
            return self.render_to_response(self.get_context_data(form=form))
        return super().form_valid(form)

    def form_invalid(self, form):
        User = get_user_model()
        try:
            user = User.objects.get(email=self.request.POST['username'])
            if not user.is_active:
                messages.error(self.request, 'Вам приостановлен доступ к сервису, обратитесь в техническую поддержку.')
        except User.DoesNotExist:
            messages.error(self.request, 'Такой пользователь не обнаружен. Вам необходимо зарегистрироваться.')

        return super().form_invalid(form)


class RegisterView(CreateView):
    """
    Представление для регистрации новых пользователей и
    отправки ссылки для подтверждения по электронной почте.
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
    """
    Обработка подтверждения электронной почты пользователя.
    """

    def get(self, request, email_verification_code):
        try:
            user = User.objects.get(email_verification_code=email_verification_code)
            user.email_verified = True
            user.save()
            messages.success(request, 'Ваша почта успешно подтверждена!')
        except User.DoesNotExist:
            messages.error(request, 'Неверная или устаревшая ссылка подтверждения.')

        return redirect('users:login')


class BlockUserView(ManagerMixin, View):
    """
    Позволяет менеджерам блокировать или разблокировать пользователей.
    """
    template_name = 'users/block_user.html'

    def get(self, request):
        form = BlockUserForm()
        User = get_user_model()

        users = User.objects.exclude(is_superuser=True).exclude(groups__name='Managers')

        return render(request, self.template_name, {'form': form, 'users': users})

    def post(self, request):
        form = BlockUserForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            try:
                User = get_user_model()
                user_to_block = User.objects.get(pk=user_id)
                user_to_block.is_active = not user_to_block.is_active
                user_to_block.save()
                print("Пользователь успешно заблокирован")
                return redirect('users:block_user')
            except User.DoesNotExist:
                form.add_error('user_id', 'Пользователь не найден.')
