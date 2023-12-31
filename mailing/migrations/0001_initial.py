# Generated by Django 4.2.5 on 2023-10-03 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='электронная почта')),
                ('name', models.CharField(max_length=250, verbose_name='ФИО')),
                ('comment', models.TextField(blank=True, max_length=250, null=True, verbose_name='комментарий')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='MailingSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('periodicity', models.CharField(choices=[('D', 'Daily'), ('W', 'Weekly'), ('M', 'Monthly')], max_length=1)),
                ('status', models.CharField(choices=[('C', 'Created'), ('R', 'Running'), ('E', 'Ended')], max_length=1)),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
        migrations.CreateModel(
            name='MailingMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('mailing_settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='mailing.mailingsettings')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='MailingLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt_time', models.DateTimeField(auto_now_add=True, verbose_name='дата последней попытки')),
                ('status', models.BooleanField(verbose_name='статус отправки')),
                ('server_response', models.TextField(blank=True, null=True, verbose_name='ответ почтового сервиса')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='mailing.client')),
                ('mailing_settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='mailing.mailingsettings')),
            ],
            options={
                'verbose_name': 'Попытка',
                'verbose_name_plural': 'Попытки',
            },
        ),
    ]
