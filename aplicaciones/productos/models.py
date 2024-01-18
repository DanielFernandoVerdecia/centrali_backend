from django.db import models

from ..users.models import *

class Productos(models.Model):

    producto = models.CharField(unique = True, max_length = 250)
    precio = models.DecimalField( max_digits = 500, decimal_places=2)
    cantidad_disponible = models.PositiveBigIntegerField(default = 0)

    creador = models.ForeignKey(
        Usuarios, null = True, blank = True, on_delete = models.SET_NULL)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null = True, blank = True)
