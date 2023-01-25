from django.db import models

# Create your models here.

class Vuelo (models.Model):
    origenVuelo = models.CharField(max_length=30, verbose_name='Origen')
    destinoVuelo = models.CharField(max_length=30, verbose_name='Destino')
    # Este queda medio dudoso, pero lo vamos a dejar aca :D
    fechaIngreso = models.DateField(verbose_name='Ingreso')
    fechaEgreso = models.DateField(verbose_name='Egreso')
    opcionVuelo = models.CharField(verbose_name='Opciones', max_length=15)
    # Este tambien anda medio medio...
    cantidadPersonas = models.IntegerField(verbose_name='Cantidad')