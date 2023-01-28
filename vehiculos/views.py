from django.shortcuts import render
from django.http import HttpResponse
from .models import Vuelo
from .forms import VueloForm

# Create your views here.

def inicio(request):
    # formulario = VueloForm(request.POST or None)
    if(request.method == 'POST'):
        new_vuelo = Vuelo(
            origenVuelo = "Sexo"
        )
        new_vuelo.save()
    return render(request, 'paginas/index.html')

# El usuario solo podra crear una instancia POST mientras este registrado, mientras el superusuario puede hacer 4 acciones: create, read, update y delete (CRUD).
def acerca(request):
    return render(request, 'paginas/acerca.html')

def login(request):
    return render(request, 'paginas/login.html')

def register(request):
    return render(request, 'paginas/register.html')