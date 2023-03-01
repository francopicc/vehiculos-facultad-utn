## Gestion de Vehiculos - Proyecto Final UTN
Este proyecto tiene como idea principal, un sitio web que permita la gestion de vehiculos. Tiene los siguientes requisitos: Python, Django, mySQL y JavaScript.

Para iniciar el proyecto, se introduce esto en la consola de comandos preferida:
```
python3 manage.py runserver localhost:8000
```

## Algunos Tips
Recomiendo antes de probar el proyecto, iniciarlo con conectividad a internet ya que posee cdn's que no provienen localmente (fuentes, etc).

Tambien puede que si estas editando el proyecto y no se muestran los cambios pueden ser por dos razones: no recargaste la pagina o solo te esta mostrando la pagina en cache (solucion: shift + f5)

El servidor con la base de datos esta en Xampp (herramienta que ya incluye mySQL, junto a otras herramientas como Apache)

## Configuracion de variables de entorno

La unica variable que existe es ```MERCADOPAGO_SAMPLE_ACCESS_TOKEN``` que se puede extraer de las credenciales de TESTEO, no de produccion.
