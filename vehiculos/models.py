from django.db import models

# Create your models here.

# Las cosas que estan comentadas son una equivocacion por parte del proyecto (se pueden borrar.)

# Modelo para recibir POST de alquileres, etc.
# OPCIONES_VUELO1 = (
#     ('allincluded', 'Todo Incluido'),
#     ('flight', 'Vuelos'),
#     ('hotel', 'Hotel'),
#     ('car', 'Auto'),
#     ('package', 'Paquete'),
# )
# OPCIONES_VUELO2 = (
#     ('hotel', 'Hotel'),
#     ('flight', 'Vuelo'),
#     ('car', 'Auto'),
# )
# OPCIONES_VUELO3= (
#     ('idavuelta', 'Ida y Vuelta'),
#     ('soloida', 'Solo Ida'),
# )
# class Vuelo (models.Model):
#     # Se podria añadir un ID aca porque es mas facil identificar el vuelo (pronto)
#     id = models.AutoField(primary_key=True)
#     tipoVuelo1 = models.CharField(max_length=60, choices=OPCIONES_VUELO1, verbose_name="Opciones Vuelo 1", default="allincluded")
#     tipoVuelo2 = models.CharField(max_length=60, choices=OPCIONES_VUELO2, verbose_name="Opciones Vuelo 2", default="hotel")
#     origenVuelo = models.CharField(max_length=30, verbose_name='Origen')
#     destinoVuelo = models.CharField(max_length=30, verbose_name='Destino')
#     fechaIngreso = models.DateField(verbose_name='Ingreso')
#     fechaEgreso = models.DateField(verbose_name='Egreso', null=True)
#     opcionVuelo = models.CharField(verbose_name='Opciones', max_length=15, choices=OPCIONES_VUELO3)
#     cantidadPersonas = models.IntegerField(verbose_name='Cantidad')

#     def __str__(self):
#         fila = self.origenVuelo + " " + self.destinoVuelo
#         return fila

# class Hotel (models.Model):
#     # Se podria añadir un ID aca porque es mas facil identificar el vuelo (pronto)
#     id = models.AutoField(primary_key=True)
#     tipoVuelo1 = models.CharField(max_length=60, choices=OPCIONES_VUELO1, verbose_name="Opciones Vuelo 1", default="allincluded")
#     tipoVuelo2 = models.CharField(max_length=60, choices=OPCIONES_VUELO2, verbose_name="Opciones Vuelo 2", default="hotel")
#     origenVuelo = models.CharField(max_length=30, verbose_name='Origen')
#     destinoVuelo = models.CharField(max_length=30, verbose_name='Destino')
#     fechaIngreso = models.DateField(verbose_name='Ingreso')
#     fechaEgreso = models.DateField(verbose_name='Egreso', null=True)
#     opcionVuelo = models.CharField(verbose_name='Opciones', max_length=15, choices=OPCIONES_VUELO3)
#     cantidadPersonas = models.IntegerField(verbose_name='Cantidad')

#     def __str__(self):
#         fila = self.origenVuelo + " " + self.destinoVuelo
#         return fila

class Auto (models.Model):
    # Se podria añadir un ID aca porque es mas facil identificar el vehiculo
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60, verbose_name="Nombre", default="")
    marca = models.CharField(max_length=25, verbose_name="Marca", default="")
    modelo = models.CharField(max_length=50, verbose_name="Modelo", default="")
    imagenes = models.ImageField(verbose_name="Imagen/es", default="", upload_to="imagenes")
    precio = models.IntegerField(verbose_name="Precio", default=0)
    proovedor = models.CharField(max_length=35, verbose_name="Proovedor", default="-")
    capacidad = models.IntegerField(verbose_name="Capacidad", default=0)
    cobertura = models.BooleanField(verbose_name="Tiene Cobertura:", default=False)
    aire_acondicionado = models.BooleanField(verbose_name="Tiene Aire Acondicionado:", default=False)
    kilometraje = models.BooleanField(verbose_name="Tiene Kilometraje:", default=False)
    reservado = models.BooleanField(verbose_name="Esta reservado:", default=False)
    lugarRetiro = models.CharField(verbose_name="Lugar de Retiro", max_length=50,default="")
    fechaRetiro = models.DateTimeField(verbose_name="Fecha de Retiro", blank=True, null=True)
    fechaRegreso = models.DateTimeField(verbose_name="Fecha de Regreso", blank=True, null=True)

    def __str__(self):
        fila = self.nombre + " - " + self.marca + " " + self.modelo
        return fila

# class Paquete (models.Model):
#     # Se podria añadir un ID aca porque es mas facil identificar el vuelo (pronto)
#     id = models.AutoField(primary_key=True)
#     tipoVuelo1 = models.CharField(max_length=60, choices=OPCIONES_VUELO1, verbose_name="Opciones Vuelo 1", default="allincluded")
#     tipoVuelo2 = models.CharField(max_length=60, choices=OPCIONES_VUELO2, verbose_name="Opciones Vuelo 2", default="hotel")
#     origenVuelo = models.CharField(max_length=30, verbose_name='Origen')
#     destinoVuelo = models.CharField(max_length=30, verbose_name='Destino')
#     fechaIngreso = models.DateField(verbose_name='Ingreso')
#     fechaEgreso = models.DateField(verbose_name='Egreso', null=True)
#     opcionVuelo = models.CharField(verbose_name='Opciones', max_length=15, choices=OPCIONES_VUELO3)
#     cantidadPersonas = models.IntegerField(verbose_name='Cantidad')

#     def __str__(self):
#         fila = self.origenVuelo + " " + self.destinoVuelo
#         return fila


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