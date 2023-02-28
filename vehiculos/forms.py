from django import forms
from .models import Auto, Account

# Formulario de POST Home

class AutoForm (forms.ModelForm):
    class Meta:
        model = Auto
        fields = '__all__'

class AccountForm (forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'surname', 'dateBirth', 'telefono', 'doc_type', 'doc_number', 'pais', 'provincia', 'calle', 'altura', 'ciudad', 'cp']