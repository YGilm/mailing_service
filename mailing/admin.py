from django.contrib import admin
from .models import Client, MailingMessage, MailingLog, MailingSettings


class ClientInline(admin.TabularInline):
    model = MailingSettings.recipients.through
    extra = 1
    fields = ('client',)


class MailingMessageInline(admin.StackedInline):
    model = MailingMessage
    extra = 1


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'comment')
    search_fields = ('name', 'email')
    list_filter = ('name',)


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'body', 'mailing_settings')
    search_fields = ('subject', 'body')
    list_filter = ('subject',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('attempt_time', 'status', 'server_response', 'client', 'mailing_settings')
    search_fields = ('attempt_time', 'status', 'server_response')
    list_filter = ('attempt_time', 'status')


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    inlines = [MailingMessageInline, ClientInline]
    list_display = ('time', 'periodicity', 'status')
    search_fields = ('time', 'periodicity', 'status')
    list_filter = ('time', 'periodicity', 'status')
    filter_horizontal = ('recipients',)
