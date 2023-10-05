from django.core.mail import send_mail
from django.utils import timezone
import os
from mailing.models import MailingSettings, Client, MailingMessage, MailingLog


def send_mailing():
    mailing = MailingSettings.objects.filter(time__lte=timezone.now(),
                                             status="R").first()
    if mailing:
        clients = Client.objects.all()
        mailing_message = MailingMessage.objects.filter(mailing_settings=mailing).first()

        for client in clients:
            try:
                send_mail(
                    mailing_message.subject,
                    mailing_message.body,
                    os.getenv('EMAIL_HOST_USER'),  # Отправитель
                    [client.email],  # Получатель
                )
                log_status = True
                server_response = "Successfully sent"
            except Exception as e:
                log_status = False
                server_response = str(e)

            # Логирование отправки
            MailingLog.objects.create(
                client=client,
                mailing_settings=mailing,
                status=log_status,
                server_response=server_response
            )

        # Меняем статус рассылки
        mailing.status = "E"
        mailing.save()
