from rest_framework import serializers
from .models import *

from ..productos.models import *

#Para formato de pesos colombianos
import locale

from datetime import datetime

class VerMesasSerializer(serializers.ModelSerializer):

    class Meta:

        model = Mesas
        fields = (
            'id',
            'nombre',
        )

class CrearMesaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Mesas
        fields = (
            'nombre',
        )

class EliminarVariasMesasSerializer(serializers.Serializer):
  
    ids = serializers.ListField(child = serializers.IntegerField())

class CrearVentaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Ventas
        fields = (
            'productos',
            'mesa',
            'venta_finalizada',
        )
    
    def create(self, validated_data):

        usuario = self.context.get('usuario')
        productos = validated_data['productos']


        info_ventas = usuario + ' ha creado una venta. Se agregó, '
        ganancia_total = 0

        #Formato pesos colombianos
        locale.setlocale(locale.LC_MONETARY, 'es_CO.UTF-8')

   
        for producto_actual in productos:

        
            producto = producto_actual['producto']  
            precio = locale.currency(producto_actual['precio'], grouping=True)  
            cantidad = str(producto_actual['cantidad'])

            #Quitamos la cantidad actual del producto
            producto_encontrado = Productos.objects.get(id = producto_actual['id'])

            if producto_encontrado.cantidad_disponible < producto_actual['cantidad']:
                    raise serializers.ValidationError(
                        {'Errors':'El producto, ' + producto_encontrado.producto + ', no cuenta con la cantidad disponible para descontar, cantidad disponible: ' + str(producto_encontrado.cantidad_disponible
                                                                                                                                                              ) + ', usted intenta descontar: ' + str(producto_actual['cantidad']) + ' unidades.'} )

            producto_encontrado.cantidad_disponible -= producto_actual['cantidad']
            producto_encontrado.save()

            ganancia_total += producto_actual['precio'] * producto_actual['cantidad']

            info_ventas += producto + ', cantidad: ' + cantidad + ', precio: ' + precio + '. '
        
        ganancia_total = round(ganancia_total, 2)

   
        #Crear nueva info_ventas
        nueva_info_ventas = Info_ventas.objects.create(descripcion = info_ventas)


                
        validated_data['info_ventas'] = [nueva_info_ventas]
        validated_data['ganancia_total'] = ganancia_total


    
        nuevo_producto = super().create(validated_data)

        return nuevo_producto

class VerInfoVentasSerializer(serializers.ModelSerializer):

    class Meta:

        model = Info_ventas
        fields = (
            '__all__'
        )


class VerVentaSerializer(serializers.ModelSerializer):

    mesa = VerMesasSerializer()
    info_ventas = VerInfoVentasSerializer(read_only=True, many=True)

    class Meta:

        model = Ventas
        fields = (
            '__all__'
        )    

class VerEditarVentaSerializer(serializers.ModelSerializer):

    mesa = VerMesasSerializer()

    class Meta:

        model = Ventas
        fields = (
            'id',
            'productos',
            'mesa',
            'venta_finalizada',
        ) 


class ActualizarVentaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Ventas
        fields = (
            'productos',
            'mesa',
            'venta_finalizada',
        )
    
    def update(self, instance , validated_data):

        usuario = self.context.get('usuario')
        productos = validated_data['productos']


        info_ventas = usuario + ' ha actualizado una venta. Se agregó, '
        ganancia_total = 0

        #Formato pesos colombianos
        locale.setlocale(locale.LC_MONETARY, 'es_CO.UTF-8')

        for producto_actual in productos:

            producto = producto_actual['producto']  
            precio = locale.currency(producto_actual['precio'], grouping=True)  
            cantidad = str(producto_actual['cantidad'])

            #Quitamos la cantidad actual del producto si realmente el usuario actualizó la cantidad del producto
            if producto_actual['editado']:

                producto_encontrado = Productos.objects.get(id = producto_actual['id'])

                if producto_encontrado.cantidad_disponible < producto_actual['cantidad']:
                    raise serializers.ValidationError(
                        {'Errors':'El producto, ' + producto_encontrado.producto + ', no cuenta con la cantidad disponible para descontar, cantidad disponible: ' + str(producto_encontrado.cantidad_disponible
                                                                                                                                                              ) + ', usted intenta descontar: ' + str(producto_actual['cantidad']) + ' unidades.'} )
                
                producto_encontrado.cantidad_disponible -= producto_actual['cantidad']
                producto_encontrado.save()

                producto_actual['editado'] = False

            ganancia_total += producto_actual['precio'] * producto_actual['cantidad']

            
            info_ventas += producto + ', cantidad: ' + cantidad + ', precio: ' + precio + '. '
        
        ganancia_total = round(ganancia_total, 2)

   
        #Crear nueva info_ventas
        nueva_info_ventas = Info_ventas.objects.create(descripcion = info_ventas)
        instance.info_ventas.add(nueva_info_ventas)
  
                
      
        validated_data['ganancia_total'] = ganancia_total

        instance.fecha_actualizacion = datetime.now()


        producto_actualizado = super().update(instance, validated_data)

        return producto_actualizado
    

class EliminarVariasVentasSerializer(serializers.Serializer):
  
    ids = serializers.ListField(child = serializers.IntegerField())