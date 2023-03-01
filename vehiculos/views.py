from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Auto, Account
from .forms import AutoForm, AccountForm
from django.contrib.sessions.backends.db import SessionStore
from django.views.decorators.csrf import csrf_exempt
import locale
session = SessionStore()
import mercadopago
from dotenv import load_dotenv
import os
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import requests

load_dotenv()

sdk = mercadopago.SDK(os.getenv("MERCADO_PAGO_SAMPLE_ACCESS_TOKEN"))

# Create your views here.

def inicio(request):
    formulario = AutoForm()
    # print(user)
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

@login_required
def details(request):
    # lista = Auto.objects.all().filter(nombre=)
    try:
        if request.method == 'POST':
            datos = request.POST.get('idFromVehiculo')
            detailsData = Auto.objects.get(id=datos)
        # Informacion que recibimos para completar la data de lugar y fecha
        placeData = {
        'placeName': request.session['lugarRetiro'],
        'retiro': request.session['fechaRetiro'],
        'regreso': request.session['fechaRegreso']
        }
    except:
        return redirect('/')
    return render(request, 'paginas/details.html', {'checkout': detailsData, 'place': placeData, 'id': datos})

@login_required
def checkout(request):
    try:
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
    except:
        return redirect('/')
    return render(request, 'paginas/checkout.html', {'checkout': checkoutData, 'place': placeData, 'price': priceDetails})

# Pagos con Tarjeta de Credito y de Debito
@login_required
@csrf_exempt
def payment(request):
    if request.method == "POST":
        try:
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
            print(payment)
            # Editamos la info del auto cuando el pago da el status approved.
            if payment["status"] == "pending":
                # Solo indicamos que alguien intento comprar el auto (pero sigue disponible)
                autos.userWhoPayed = str(User.objects.get(username=request.user.username))
                autos.status = payment["status"]
                autos.save()
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
                autos.status = payment["status"]
                autos.userWhoPayed = str(User.objects.get(username=request.user.username))
                autos.save()
        except KeyError as e:
            return redirect('/')
    return render(request, 'paginas/payment.html', {"status": payment["status"], "description": payment["description"], "payment_method": payment["payment_method_id"], "payment_type": payment["payment_type_id"], "price": payment["transaction_amount"], "cardFirstNumbers": payment["card"]["last_four_digits"], "dni": payment["card"]["cardholder"]["identification"]["number"], "name": payment["card"]["cardholder"]["name"]})

# Pagos con RapiPago y PagoFacil
@login_required
@csrf_exempt
def paymentrapi (request):
    # Pasar precio final y cosas que faltan
    if request.method == 'POST':
        try:
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
            if payment["status"] == "pending":
                car_id = request.POST.get("idCarVehiculo")
                print(car_id)
                autos = Auto.objects.get(id=car_id)
                # Solo indicamos que alguien intento comprar el auto (pero sigue disponible)
                autos.userWhoPayed = str(User.objects.get(username=request.user.username))
                autos.status = payment["status"]
                autos.idPayment = payment["id"]
                autos.save()

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
                # lanzamos el status approved
                autos.status = payment["status"]
                autos.userWhoPayed = str(User.objects.get(username=request.user.username))
                autos.save()
        except KeyError as e:
            return redirect('/')
    return render(request, 'paginas/payment_rapi.html', {"status": payment["status"], "description": payment["description"], "payment_method": payment["payment_method_id"], "price": payment["transaction_amount"], "url": payment["transaction_details"]["external_resource_url"]})

# Parte Usuarios - Registro

@csrf_exempt
def register(request):
    accountf = AccountForm()
    if request.method == 'POST':
        accountf = AccountForm(request.POST or None)
        if accountf.is_valid():
            try:
                userTest = User.objects.create_user(
                    username = request.POST.get("email"),
                    password = request.POST.get("password"),
                    first_name = request.POST.get("name"),
                    last_name= request.POST.get("surname"),
                )
                userTest.save()
                accountf.save()
                auth_login(request, userTest)
                return redirect('/')
            except IntegrityError():
                return HttpResponse("La cuenta tuvo errores al crear")
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'paginas/register.html', {'formulario': accountf})

# Cerrar Sesion

@login_required
def signout(request):
    logout(request)
    return redirect('/')

# Login

def login(request):
    if request.method == 'GET':
        return render(request, 'paginas/login.html')
    else:
        user = authenticate(request, username = request.POST["email"], password = request.POST["password"])
        if user is None:
            return HttpResponse("Error")
        else:
            auth_login(request, user)
            return redirect('/')
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'paginas/login.html')

@login_required
def compras(request):
    if request.method == 'GET':
        username = str(User.objects.get(username=request.user.username))
        vehiculo = Auto.objects.filter(userWhoPayed=username)

    return render(request, 'paginas/compras.html', {'compra': vehiculo})

@login_required
def compras_details(request, or_id):
    # enviar por post mediante un form
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        usernameToCheck = str(User.objects.get(username=request.user.username))
        print(usernameToCheck)
        idToCheck = request.POST["check_id"]
        vehiculo = Auto.objects.filter(idPayment=idToCheck)
        if str(usernameToCheck) in str(vehiculo[0]):
            return redirect('/')
    return render(request, 'paginas/orderDetails.html')