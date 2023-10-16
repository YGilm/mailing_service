from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import path, reverse_lazy, include
from . import views
from .apps import UsersConfig
from .views import RegisterView, EmailVerificationView, BlockUserView
from django.contrib.auth import views as auth_views

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/<uuid:email_verification_code>/', EmailVerificationView.as_view(), name='email_verification'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(template_name='users/password_reset_form.html',
                                                      email_template_name="users/password_reset_email.html",
                                                      from_email=settings.EMAIL_HOST_USER,
                                                      success_url=reverse_lazy('users:password_reset_done')),
         name='update_password'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                                     success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('block_user/', BlockUserView.as_view(), name='block_user'),

]
