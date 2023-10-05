from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='электронная почта')
    name = models.CharField(max_length=250, verbose_name='ФИО')
    comment = models.TextField(max_length=250, verbose_name='комментарий', **NULLABLE)

    def __str__(self):
        return f'{self.name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailingSettings(models.Model):
    TIME_CHOICES = [('D', 'Daily'), ('W', 'Weekly'), ('M', 'Monthly')]
    STATUS_CHOICES = [('C', 'Created'), ('R', 'Running'), ('E', 'Ended')]

    time = models.DateTimeField()
    periodicity = models.CharField(max_length=1, choices=TIME_CHOICES)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return f'{self.time}, {self.periodicity}, {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingMessage(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    mailing_settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MailingLog(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='logs')
    mailing_settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, related_name='logs')
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='дата последней попытки')
    status = models.BooleanField(verbose_name='статус отправки')
    server_response = models.TextField(verbose_name='ответ почтового сервиса', **NULLABLE)

    def __str__(self):
        return f'{self.status} ({self.attempt_time})'

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'
