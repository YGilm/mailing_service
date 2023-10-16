from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views import View
from django.views.generic.edit import CreateView
from .models import User
from .forms import UserRegisterForm, BlockUserForm
from . import services


class ManagerOrSuperuserMixin:
    # Функция для проверки, является ли пользователь менеджером или суперпользователем.
    def is_manager_or_superuser(self):
        return self.request.user.is_authenticated and (self.request.user.is_superuser or self.request.user.is_manager)


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


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return redirect('home_page')
#             else:
#                 messages.error(request, 'Ваш аккаунт заблокирован. Обратитесь в техническую поддержку.')
#                 return redirect('users:login')
#         else:
#             messages.error(request, 'Неверный логин или пароль.')
#             return redirect('users:login')


class BlockUserView(ManagerOrSuperuserMixin, View):
    template_name = 'users/block_user.html'

    def get(self, request):
        form = BlockUserForm()
        users = get_user_model().objects.all()
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
                print("User blocked successfully")
                return redirect('users:block_user')
            except User.DoesNotExist:
                form.add_error('user_id', 'Пользователь не найден.')
