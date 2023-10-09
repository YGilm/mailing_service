from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django import forms
from .models import MailingSettings, Client, MailingMessage


class MailingForm(forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = ['time', 'periodicity', 'status', 'recipients']
        widgets = {
            'time': DateTimePickerInput(format='%Y-%m-%d %H:%M:%S'),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'name', 'comment']


class MailingMessageForm(forms.ModelForm):
    class Meta:
        model = MailingMessage
        fields = ['subject', 'body']
