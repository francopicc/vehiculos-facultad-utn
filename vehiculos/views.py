from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Auto
from .forms import AutoForm
from django.contrib.sessions.backends.db import SessionStore
from django.views.decorators.csrf import csrf_exempt
import locale
session = SessionStore()
import mercadopago
from dotenv import load_dotenv
import os
from django.contrib.auth.forms import UserCreationForm

load_dotenv()

sdk = mercadopago.SDK(os.getenv("MERCADO_PAGO_SAMPLE_ACCESS_TOKEN"))

# Create your views here.

def inicio(request):
    formulario = AutoForm()
    if request.method == 'POST':
        if formulario.is_valid:
            formulario = AutoForm(request.POST)
            # Algunas variables de sesion que nos ayudaran a obtener los datos en el check-out.
            request.session['lugarRetiro'] = request.POST.get("lugarRetiro")
            request.session['fechaRetiro'] = request.POST.get("fechaRetiro")
            request.session['fechaRegreso'] = request.POST.get("fechaRegreso")
    # Obtencion de todos los datos de la db "autos"
    lista = Auto.objects.all().filter(reservado=False)
    return render(request, 'paginas/index.html', {'formulario': formulario, 'datos': lista})

# El usuario solo podra crear una instancia POST mientras este registrado, mientras el superusuario puede hacer 4 acciones: create, read, update y delete (CRUD).
def acerca(request):
    return render(request, 'paginas/acerca.html')

def login(request):
    return render(request, 'paginas/login.html')

def details(request):
    # lista = Auto.objects.all().filter(nombre=)
    if request.method == 'POST':
        datos = request.POST.get('idFromVehiculo')
        detailsData = Auto.objects.get(id=datos)
    # Informacion que recibimos para completar la data de lugar y fecha
    placeData = {
        'placeName': request.session['lugarRetiro'],
        'retiro': request.session['fechaRetiro'],
        'regreso': request.session['fechaRegreso']
    }
    return render(request, 'paginas/details.html', {'checkout': detailsData, 'place': placeData, 'id': datos})

def checkout(request):
    if request.method == 'POST':
        datos = request.POST.get('idFromVehiculo')
        checkoutData = Auto.objects.get(id=datos)
    # Detalles del lugar seleccionado en el form de home
    placeData = {
        'placeName': request.session['lugarRetiro'],
        'retiro': request.session['fechaRetiro'],
        'regreso': request.session['fechaRegreso']
    }
    # Precios retirados de la pagina 'details'
    priceDetails = {
        'precioximp': request.POST.get("precioFinal"),
        'precioimp': request.POST.get("precioImpuestos")
    }
    request.session['preciofinalcheckout'] = float(request.POST.get("precioFinal")) + float(request.POST.get("precioImpuestos"))
    return render(request, 'paginas/checkout.html', {'checkout': checkoutData, 'place': placeData, 'price': priceDetails})


# Pagos con Tarjeta de Credito y de Debito
@csrf_exempt
def payment(request):
    if request.method == "POST":
        payment_methods_response = sdk.payment_methods().list_all()
        payment_methods = payment_methods_response["response"]
        payment_data = {
            "transaction_amount": float(request.POST.get("transactionAmount")),
            "token": request.POST.get("token"),
            "description": request.POST.get("description"),
            "installments": int(request.POST.get("installments")),
            "payment_method_id": request.POST.get("paymentMethodId"),
            "payer": {
                "email": request.POST.get("email"),
                "identification": {
                    "type": request.POST.get("identificationType"), 
                    "number": request.POST.get("identificationNumber")
                }
            }
        }
        payment_response = sdk.payment().create(payment_data)
        payment = payment_response["response"]
        # Editamos la info del auto cuando el pago da el status approved.
        if payment["status"] == "approved":
            car_id = request.POST.get("idCarVehiculo")
            placeData = {
                'placeName': request.session['lugarRetiro'],
                'retiro': request.session['fechaRetiro'],
                'regreso': request.session['fechaRegreso']
            }
            autos = Auto.objects.get(id=car_id)
            autos.reservado = True
            autos.fechaRetiro = placeData["retiro"]
            autos.fechaRegreso = placeData["regreso"]
            autos.idPayment = payment["id"]
            autos.save()
        
    return render(request, 'paginas/payment.html', {"status": payment["status"], "description": payment["description"], "payment_method": payment["payment_method_id"], "payment_type": payment["payment_type_id"], "price": payment["transaction_amount"], "cardFirstNumbers": payment["card"]["last_four_digits"], "dni": payment["card"]["cardholder"]["identification"]["number"], "name": payment["card"]["cardholder"]["name"]})

# Pagos con RapiPago y PagoFacil

@csrf_exempt
def paymentrapi (request):
    # Pasar precio final y cosas que faltan
    if request.method == 'POST':
        price_data = {
            "price": request.session['preciofinalcheckout']
        }
        payment_data = {
            "transaction_amount": int(price_data["price"]),
            "description": request.POST.get("description"),
            "payment_method_id": request.POST.get("paymentMethod_ID"),
            "payer": {
                "email": request.POST.get("email")
            }
        }
        payment_response = sdk.payment().create(payment_data)
        payment = payment_response["response"]
        print(payment)
        if payment["status"] == "approved":
            car_id = request.POST.get("idCarVehiculo")
            placeData = {
                'placeName': request.session['lugarRetiro'],
                'retiro': request.session['fechaRetiro'],
                'regreso': request.session['fechaRegreso']
            }
            autos = Auto.objects.get(id=car_id)
            autos.reservado = True
            autos.fechaRetiro = placeData["retiro"]
            autos.fechaRegreso = placeData["regreso"]
            autos.idPayment = payment["id"]
            autos.save()
            
    return render(request, 'paginas/payment_rapi.html', {"status": payment["status"], "description": payment["description"], "payment_method": payment["payment_method_id"], "price": payment["transaction_amount"], "url": payment["transaction_details"]["external_resource_url"]})

def register(request):
    return render(request, 'paginas/register.html')