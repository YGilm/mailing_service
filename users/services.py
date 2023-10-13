from django.core.mail import send_mail
from config import settings


def send_verification(email: str, url: str):
    """
    Функция для отправки ссылки верификации на почту
    """

    send_mail(
        subject='Your verification code',
        message=f'to confirm registration, follow the link:\n '
                f'{url}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
