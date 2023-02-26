from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('acerca', views.acerca, name='acerca'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('order/details', views.details, name='details'),
    path('order/checkout', views.checkout, name='checkout'),
    path('order/success_card', views.payment, name='payment'),
    path('order/success_cash', views.paymentrapi, name="payment-rapi"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)