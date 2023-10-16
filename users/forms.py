from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
from users.models import User


class UserRegisterForm(UserCreationForm):
    """Форма для регистрации пользователя"""

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].help_text = None


class BlockUserForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())


