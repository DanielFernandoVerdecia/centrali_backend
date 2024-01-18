from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UsuarioManager

class Usuarios(AbstractBaseUser, PermissionsMixin):
    
    nombre = models.CharField(max_length = 50, unique = True)
    email = models.EmailField(unique = True)
    password = models.CharField(null = True, blank = True)
    is_active = models.BooleanField(default = False)
    activo_con_email_password = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    cargo = models.CharField(max_length = 50, default = 'Empleado')
    fecha_creacion = models.DateTimeField(null = True, blank = True, auto_now_add=True)

    
    codigo_recuperar_cuenta = models.CharField(
        unique = True, 
        null = True,
        blank = True
    )


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    objeto = UsuarioManager()
    objects = models.Manager()

    def get_name(self):

        return self.nombre

class Configuracion(models.Model):

    restriccion_cuenta_empleados = models.BooleanField(default = False)
    
