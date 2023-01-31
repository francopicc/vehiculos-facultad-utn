from django import forms
from .models import Auto

# Formulario de POST Home

class AutoForm (forms.ModelForm):
    class Meta:
        model = Auto
        fields = '__all__'