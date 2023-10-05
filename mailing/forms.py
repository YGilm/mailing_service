from django import forms
from .models import MailingSettings


class MailingForm(forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = ['time', 'periodicity', 'status']
