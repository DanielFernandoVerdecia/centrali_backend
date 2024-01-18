from django.db import models


class Mesas(models.Model):
   
   nombre = models.CharField(unique = True, blank = False, null = False)

class Info_ventas(models.Model):
   
   descripcion = models.TextField()

class Ventas(models.Model):

   productos = models.JSONField()
   mesa = models.ForeignKey(Mesas, on_delete = models.SET_NULL, null = True)
   info_ventas = models.ManyToManyField(Info_ventas)
   ganancia_total = models.DecimalField(max_digits = 500, decimal_places=2)
   venta_finalizada = models.BooleanField(default = False)
   fecha_creacion = models.DateTimeField(auto_now_add=True)
   fecha_actualizacion = models.DateTimeField(null = True, blank = True, 
                                              default = None)
   