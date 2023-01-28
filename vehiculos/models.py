from django.db import models

# Create your models here.

# Modelo para recibir POST de alquileres, etc.

class Vuelo (models.Model):
    # Se podria añadir un ID aca porque es mas facil identificar el vuelo (pronto)
    id = models.AutoField(primary_key=True)
    tipoVuelo1 = models.BooleanField(default=False, verbose_name="Opciones de Input 1")
    tipoVuelo2 = models.BooleanField(default=False, verbose_name="Opciones de Input 2")
    origenVuelo = models.CharField(max_length=30, verbose_name='Origen')
    destinoVuelo = models.CharField(max_length=30, verbose_name='Destino')
    # Este queda medio dudoso, pero lo vamos a dejar aca :D
    fechaIngreso = models.DateField(verbose_name='Ingreso', null=False)
    fechaEgreso = models.DateField(verbose_name='Egreso', null=False)
    opcionVuelo = models.CharField(verbose_name='Opciones', max_length=15)
    # Este tambien anda medio medio...
    cantidadPersonas = models.IntegerField(verbose_name='Cantidad')

    def __str__(self):
        fila = self.origenVuelo + " " + self.destinoVuelo
        return fila


# Modelo para recibir cada dato del usuario. Pueden encontrarse superusuarios y usuarios.

# Arreglar comillas doble por una comilla (mas simple)

class User (models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=30)
    apellido = models.CharField(verbose_name='Apellido', max_length=30)
    nacimiento = models.DateField(verbose_name="Nacimiento")
    telefono = models.IntegerField(verbose_name='Telefono')
    tipodocumento = models.CharField(verbose_name='Tipo DNI', max_length=15)
    documento = models.IntegerField(verbose_name="Documento")
    pais = models.CharField(verbose_name="Pais", max_length=40)
    provincia = models.CharField(verbose_name="Provincia", max_length=25)
    calle = models.CharField(verbose_name="Calle", max_length=40)
    altura = models.CharField(verbose_name="Altura", max_length=20)
    ciudad = models.CharField(verbose_name="Ciudad", max_length=30)
    cp = models.CharField(verbose_name="Codigo Postal", max_length=10)