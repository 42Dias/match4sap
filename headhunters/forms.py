from django.forms import ModelForm

from localflavor.br.forms import (BRStateChoiceField, BRCNPJField, BRCPFField,
    BRZipCodeField)

from .models import Job, Headhunter

class ConnectionForm(ModelForm):
    state = BRStateChoiceField()

    class Meta:
        model = Job
        fields = [
            'title',
            'state',
            'working_years', 
            'implementations', 
            'supports', 
            'modules', 
            'industries',
            'methodology',
        ]
        labels = {
            'title': 'titulo da busca',
            'working_years': 'anos de experiência',
            'supports': 'número de suportes',
            'implementations': 'número de implantações',
        }

    def save(self, commit=True):
        connection = super().save(commit=False)
        connection.state = self.cleaned_data['state']
        if commit:
            connection.save()
        return connection


class TokensForm(ModelForm):
    cpf = BRCPFField(required=False, max_length=14, min_length=11)
    cnpj = BRCNPJField(required=False, min_length=16)
    cep = BRZipCodeField()

    class Meta:
        model = Headhunter
        fields = '__all__'
        labels = {
            'address': 'Endereço',
            'address2': '',
        }

    def __init__(self, *args, **kwargs):
        super(TokensForm, self).__init__(*args, **kwargs)

        # add custom error messages
        self.fields['cnpj'].error_messages.update({
            'invalid': 'CNPJ inválido',
            'max_digits': 'CNPJ requer pelo menos 14 dígitos',
        })

        self.fields['cpf'].error_messages.update({
            'invalid': 'CPF inválido',
            'max_digits': 'CPF requer pelo menos 11 dígitos ou 14 caracteres',
        })