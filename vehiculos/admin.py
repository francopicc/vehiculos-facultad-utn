from django.contrib import admin
from .models import Auto, Account
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.

# Registro de Modelos para ingresos.

admin.site.register(Auto) # Auto

# Modificacion del modelo del usuario en Django Admin (Ventajas: Contraseña Cifrada)

class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = "Accounts"

class CustomizedUserAdmin(UserAdmin):
    inlines = (AccountInline, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
admin.site.register(Account)