from django import forms
from .models import Vuelo

# Formulario de POST Home

class VueloForm(forms.ModelForm):
    class Meta:
        model = Vuelo
        fields = '__all__'