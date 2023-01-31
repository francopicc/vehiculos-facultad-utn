from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Auto
from .forms import AutoForm

# Create your views here.

def inicio(request):
    formulario = AutoForm()
    lista = Auto.objects.all().filter(reservado=False)
    return render(request, 'paginas/index.html', {'formulario': formulario, 'datos': lista})

# El usuario solo podra crear una instancia POST mientras este registrado, mientras el superusuario puede hacer 4 acciones: create, read, update y delete (CRUD).
def acerca(request):
    return render(request, 'paginas/acerca.html')

def login(request):
    return render(request, 'paginas/login.html')

def register(request):
    return render(request, 'paginas/register.html')