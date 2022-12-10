from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('acerca', views.acerca, name='acerca'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register')
]