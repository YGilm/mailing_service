from django.contrib import admin

from django.contrib import admin
from .models import Client, MailingMessage, MailingLog, MailingSettings


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'comment')
    search_fields = ('name', 'email')
    list_filter = ('name',)


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'body', 'mailing_settings')
    search_fields = ('subject',)
    list_filter = ('subject',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('attempt_time', 'status', 'server_response', 'client', 'mailing_settings')
    search_fields = ('attempt_time', 'status', 'server_response')
    list_filter = ('attempt_time', 'status')


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('time', 'periodicity', 'status')
    search_fields = ('time', 'periodicity', 'status')
    list_filter = ('time', 'periodicity', 'status')
