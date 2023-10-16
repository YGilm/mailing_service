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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MailingForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['recipients'].queryset = Client.objects.filter(owner=user)



class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'name', 'comment']


class MailingMessageForm(forms.ModelForm):
    subject = forms.CharField(label='Тема')
    body = forms.CharField(label='Сообщение', widget=forms.Textarea)

    class Meta:
        model = MailingMessage
        fields = ['subject', 'body']

