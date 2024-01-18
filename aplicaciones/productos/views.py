from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status

from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.postgres.search import TrigramSimilarity

from rest_framework.permissions import IsAuthenticated
from ..permission_class import *

from .serializer import *

from .models import *

class CrearProductoVista(APIView):

    permission_classes = [IsAuthenticated, IsActiveUserPermission]

    def post(self, request, *args, **kwargs):

       access_token = request.headers.get('Authorization').split(' ')[-1] 

      
       if not access_token:
            
        return Response({
           'Errors': "No se ha proporcionado un token de acceso"
           
        })          
       
    
       token = AccessToken(access_token)
       usuario_id = token.payload['user_id']
       usuario = Usuarios.objeto.get(id = usuario_id)
       serializer = CrearProductoSerializer(data = request.data, context = {'usuario': usuario})

       if serializer.is_valid():
          
          serializer.save()

          return Response({
             "respuesta": "Nuevo producto creado"
          }, status = status.HTTP_200_OK)

       else:
        
        return Response({
            "Errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class VerProductosVista(APIView):
  
  permission_classes = [IsAuthenticated, IsActiveUserPermission]
  
  def get(self, request , *args, **kwargs):
    
   try:

      productos = Productos.objects.all()

      
      paginator = PageNumberPagination()
      result_page = paginator.paginate_queryset(productos, request)
      
      serializers = VerProductosSerializer(result_page, many=True)

      total_paginas = paginator.page.paginator.num_pages
      
      return paginator.get_paginated_response({

            'total_paginas': total_paginas,
            'datos': serializers.data

      })

   except Exception as e:
      return Response({"Errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class IdProductosVista(APIView):

    permission_classes = [IsAuthenticated, IsActiveUserPermission]

    def get(self, request, *args, **kwargs):
        try:
            productos = Productos.objects.all()
        
            id_productos = [producto.id for producto in productos]
            
            return Response({
                'respuesta': id_productos
            })

        except Exception as e:
            return Response({"Errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerProductoPorIdVista(APIView):
  
  permission_classes = [IsAuthenticated, IsActiveUserPermission]
  
  def get(self, request, *args, **kwargs):
        
        try:

            id_producto = kwargs['id']

            producto = Productos.objects.get(id = id_producto)

            serializers = VerProductoPorIdSerializer(producto)

            return Response({
                'respuesta': serializers.data
            })

        except Productos.DoesNotExist:

            return Response({
                "Errors": "Producto no encontrado"
            }, status = status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"Errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ActualizarProductoPorIDVista(APIView):

    permission_classes = [IsAuthenticated, IsActiveUserPermission]

    def put(self, request, *args, **kwargs):

        try:

            id = kwargs['id']
            producto = Productos.objects.get(id = id)
        
        except Productos.DoesNotExist:

            return Response({"Errors": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ActualizarProductoPorIdSerializer(producto, data = request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class EliminarProductoPorIdVista(APIView):

    permission_classes = [IsAuthenticated, IsActiveUserPermission]

    def delete(self, data, *args, **kwargs):

        id = kwargs['id']

        try:

            producto = Productos.objects.get(id = id)
            producto.delete()

            return Response ({
            'respuesta': 'Producto eliminado'
            }, status = status.HTTP_200_OK)

        except Productos.DoesNotExist:

            return Response({
                'Errors': "El producto no existe"
            }, status = status.HTTP_404_NOT_FOUND)
        

class EliminarVariosProductosVista(APIView):
  
  permission_classes = [IsAuthenticated, IsActiveUserPermission]

  def delete(self, request):
        
    
        serializer = EliminarVariosProductosPorIdSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        ids = serializer.validated_data.get('ids', [])

        if not ids:
            return Response({"Errors": "No se proporcionaron IDS para eliminar"}, status=status.HTTP_400_BAD_REQUEST)

        
        registros_eliminados = Productos.objects.filter(id__in=ids).delete()

        
        if registros_eliminados[0] > 0:
            return Response({"respuesta":  "Productos eliminados correctamente"}, status=status.HTTP_200_OK)
        else:
            return Response({"Errors": "No se encontraron productos para eliminar"}, status=status.HTTP_404_NOT_FOUND)
        

class BuscarProductosPorNombreVista(APIView):
  
  permission_classes = [IsAuthenticated, IsActiveUserPermission]

  def get(self, request):
          
        producto = request.query_params.get('producto', '')

        if not producto:
            
            return Response({"Errors": "No se proporcionó el nombre"}, status=status.HTTP_400_BAD_REQUEST)

        try:

            productos_encontrados = Productos.objects.filter(
                producto__trigram_similar = producto
            )

            
            if not productos_encontrados.exists():
                return Response({"Errors": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)



            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(productos_encontrados, request)
            
            serializers = VerProductosSerializer(result_page, many=True)

            total_paginas = paginator.page.paginator.num_pages
            
            return paginator.get_paginated_response({

                'total_paginas': total_paginas,
                'datos': serializers.data

            })    
      
          

        except Exception as e:
            return Response({"Errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)