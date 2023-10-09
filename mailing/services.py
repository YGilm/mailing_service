from django.core.mail import send_mail
from django.utils import timezone
import os

from config import settings
from mailing.models import MailingSettings, Client, MailingMessage, MailingLog


def send_mailing():
    print("Отправляется рассылка")
    mailings = MailingSettings.objects.filter(time__lte=timezone.now(), status="R")
    print(f"Найдена {mailings.count()} рассылка для отправки.")
    for mailing in mailings:
        print(f"Обработка рассылки: {mailing}")
        clients = mailing.recipients.all().distinct()
        mailing_message = MailingMessage.objects.filter(mailing_settings=mailing).first()

        if not mailing_message:
            print(f"Не найдено сообщение для отправки: {mailing}")
            continue

        recipients_emails = [client.email for client in clients]
        print(f"Отправка рассылки на почту: {len(recipients_emails)} получателя.")

        for client in clients:
            try:
                send_mail(
                    mailing_message.subject,
                    mailing_message.body,
                    os.getenv(settings.EMAIL_HOST_USER),  # Отправитель
                    [client.email],  # Получатель
                )
            except Exception as e:
                log_status = False
                server_response = str(e)
                # Здесь вы можете добавить дополнительное логирование ошибок
                print(f"Ошибка отправки рассылки на {client.email}: {e}")

            # Логирование отправки
            MailingLog.objects.create(
                client=client,
                mailing_settings=mailing,
                status=log_status,
                server_response=server_response
            )
        mailing.status = "E"
        mailing.save()
