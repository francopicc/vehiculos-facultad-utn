from django.db import models
from django.contrib.auth.models import User

# Create your models here.

OPCIONES_DOCUMENTO = (
     ('dni', 'DNI'),
     ('a', 'A'),
     ('b', 'B'),
     ('c', 'C'),
     ('d', 'D'),
)

OPCIONES_PAIS = (
     ('arg', 'Argentina'),
     ('a', 'A'),
     ('b', 'B'),
     ('c', 'C'),
     ('d', 'D'),
)

OPCIONES_PROVINCIA = (
     ('bsas', 'Buenos Aires'),
     ('a', 'A'),
     ('b', 'B'),
     ('c', 'C'),
     ('d', 'D'),
)

OPCIONES_CIUDAD = (
     ('bsas', 'Buenos Aires'),
     ('a', 'A'),
     ('b', 'B'),
     ('c', 'C'),
     ('d', 'D'),
)

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
    puertas = models.IntegerField(verbose_name="Cantidad de Puertas")
    automatico = models.BooleanField(verbose_name="Transmision Automatica")
    reservado = models.BooleanField(verbose_name="Esta reservado:", default=False)
    lugarRetiro = models.CharField(verbose_name="Lugar de Retiro", max_length=50,default="", null=True)
    fechaRetiro = models.DateTimeField(verbose_name="Fecha de Retiro", blank=True, null=True)
    fechaRegreso = models.DateTimeField(verbose_name="Fecha de Regreso", blank=True, null=True)
    # El idPayment servira para extraer los datos del pago una vez que estemos en la pestaña del perfil para ver los detalles.
    idPayment = models.CharField(verbose_name="ID del pago", blank=True, null=True, max_length=50)
    userWhoPayed = models.CharField(verbose_name="Comprador", blank=True, null=True, max_length=40)

    def __str__(self):
        fila = self.nombre + " - " + self.marca + " " + self.modelo
        return fila

class Account (models.Model):
     id = models.AutoField(primary_key=True)
     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="Account")
     name = models.CharField(verbose_name="Nombre", max_length=40)
     surname = models.CharField(verbose_name="Apellido", max_length=40)
     dateBirth = models.DateField(verbose_name="Fecha de Nacimiento")
     telefono = models.CharField(verbose_name="Numero de Telefono", max_length=40)
     doc_type = models.CharField(verbose_name="Tipo de Documento", choices=OPCIONES_DOCUMENTO, max_length=25)
     doc_number = models.CharField(verbose_name="Numero de Documento", max_length=40)
     pais = models.CharField(verbose_name="Pais", choices=OPCIONES_PAIS, max_length=25)
     provincia = models.CharField(verbose_name="Provincia", choices=OPCIONES_PROVINCIA, max_length=25)
     calle = models.CharField(verbose_name="Calle", max_length=20)
     altura = models.CharField(verbose_name="Altura", max_length=5, null=True, blank=True)
     ciudad = models.CharField(verbose_name="Ciudad", choices=OPCIONES_CIUDAD, max_length=25)
     cp = models.CharField(verbose_name="Codigo Postal", max_length=7)

     def __str__(self):  
          return str(self.id) + " " + self.name + self.surname