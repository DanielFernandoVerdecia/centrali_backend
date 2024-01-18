from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from ..users.models import *

from datetime import datetime

class CrearProductoSerializer(serializers.ModelSerializer):

    class Meta:

       model = Productos
       fields = (
           'producto',
           'precio',
           'cantidad_disponible',
       ) 

    def create(self, validated_data):

        usuario = self.context.get('usuario')

        validated_data['creador'] = usuario

        validated_data['fecha_actualizacion'] = None

        nuevo_producto = super().create(validated_data)

        return nuevo_producto

class CreadorSerializer(serializers.ModelSerializer):

    class Meta:

        model = Usuarios
        fields = (
            'id',
            'nombre',
            'cargo'
        )

class VerProductosSerializer(serializers.ModelSerializer):

    creador = CreadorSerializer()

    class Meta:

        model = Productos
        fields = (
            'id',
            'producto', 
            'precio',
            'cantidad_disponible',
            'creador',
            'fecha_creacion',
            'fecha_actualizacion'
        )
      
class VerProductoPorIdSerializer(serializers.ModelSerializer):

    class Meta:

        model = Productos
        fields = (
            'id',
            'producto', 
            'precio',
            'cantidad_disponible',
        )

class ActualizarProductoPorIdSerializer(serializers.ModelSerializer):

    class Meta:

        model = Productos
        fields = (
            'producto', 
            'precio',
            'cantidad_disponible',
        )

    def update(self, instance, validated_data):

        instance.producto = validated_data.get('producto', instance.producto)
        instance.precio = validated_data.get('precio', instance.precio)
        instance.cantidad_disponible = validated_data.get('cantidad_disponible', instance.cantidad_disponible)

        instance.fecha_actualizacion = datetime.now()

        instance.save()

        return instance

class EliminarVariosProductosPorIdSerializer(serializers.Serializer):

    ids = serializers.ListField(child = serializers.IntegerField())

        