from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from localflavor.br.forms import BRStateChoiceField

class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': 'As senhas não coincidem',
    }

    state = BRStateChoiceField(required=True)
    phone = forms.CharField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name', 'state', 'phone')
        labels = {
            'username': 'Nome de usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # Custom fields labels
        self.fields['phone'].label = 'Telefone/Celular'
        self.fields['state'].label = 'Estado'

        # Error messages
        self.fields['username'].error_messages.update({
            'unique': 'Esse usuário já existe',
        })
        self.fields['email'].error_messages.update({
            'unique': 'E-mail já cadastrado',
        })
        self.fields['phone'].error_messages.update({
            'unique': 'Número de telefone já cadastrado',
        })

    def save(self, commit=False):
        user = super().save(commit=False)
        user.state = self.cleaned_data['state']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username')
