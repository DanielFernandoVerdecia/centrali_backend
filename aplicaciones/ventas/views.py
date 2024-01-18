from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.contrib.postgres.search import TrigramSimilarity

from rest_framework_simplejwt.tokens import AccessToken

from rest_framework.permissions import IsAuthenticated
from ..permission_class import *

from ..users.models import *

from rest_framework.response import Response
from rest_framework import status
from .models import *

from datetime import datetime

from .serializer import *

class VerMesasVista(APIView):

    permission_classes = [IsAuthenticated, IsActiveUserPermission]

    def get(self, request, *args, **kwargs):

        try:


            mesas = Mesas.objects.all()

            paginator = PageNumberPagination()
            resultado_paginas = paginator.paginate_queryset(mesas, request)    
            
            serializer = VerMesasSerializer(resultado_paginas, many = True)

            total_paginas = paginator.page.paginator.num_pages

            return paginator.get_paginated_response(
               {
                    'total_paginas': total_paginas,
                    'datos': serializer.data
                }
           )
        
        except Exception as e:

            return Response({
                'Errors': str(e)
            }, status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class BuscarMesaPorNombreVista(APIView):

    permission_classes = [IsAuthenticated, IsActiveUserPermission]

    def get(self, request, *args, **kwargs):

        mesa = request.query_params.get('mesa', '')

        if not mesa:

            return Response({
                'Errors': 'La mesa no fue proporcionada'
            }, status = status.HTTP_400_BAD_REQUEST)

        try:

            mesa_encontrada = Mesas.objects.filter(
                nombre__trigram_similar = mesa
            ).order_by('nombre')

            if not mesa_encontrada.exists():

                return Response({
                    'Errors': 'No se encontró ninguna mesa'
                }, status = status.HTTP_404_NOT_FOUND)
            


            paginator = PageNumberPagination()
            resultado_paginas = paginator.paginate_queryset(mesa_encontrada, request)

            serializer = VerMesasSerializer(resultado_paginas, many = True)

            total_paginas = paginator.page.paginator.num_pages

            return paginator.get_paginated_response(
                {
                'total_paginas': total_paginas,
                'datos': serializer.data
            }
            )  
        
        except Exception as e:

            return Response(
                {'Errors': str(e),
                },
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class CrearMesaVisa(APIView):

    permission_classes = [IsAuthenticated, IsActiveUserPermission]

    def post(self, request, *args, **kwargs):

        serializer = CrearMesaSerializer(data = request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({
                'data': 'Mesa creada con éxito'
            }, status = status.HTTP_201_CREATED)
        
        return Response({
            'Errors': serializer.errors
        }, status = status.HTTP_400_BAD_REQUEST)

class VerMesaPorIdVista(APIView):

    permission_classes = [IsAuthenticated, IsActiveUserPermission]

    def get(self, request, *args, **kwargs):

        try:

            id_mesa = kwargs['id']

            mesa = Mesas.objects.get(id = id_mesa)

            serializers = VerMesasSerializer(mesa)

            return Response({
                'respuesta': serializers.data
            })

        except Mesas.DoesNotExist:

            return Response({
                "Errors": "Mesa no encontrada"
            }, status = status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"Errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

class EditarMesaVista(APIView):

    permission_classes = [IsAuthenticated, IsActiveUserPermission]

    def put(self, request, *args, **kwargs):

        try:

            id = kwargs['id']
            mesa = Mesas.objects.get(id = id)
        
        except Mesas.DoesNotExist:

            return Response({"Errors": "Mesa no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = VerMesasSerializer(mesa, data = request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class EliminarMesaPorIdVista(APIView):

    permission_classes = [IsAuthenticated, IsActiveUserPermission]

    def delete(self, data, *args, **kwargs):

        id = kwargs['id']

        try:

            mesa = Mesas.objects.get(id = id)
            mesa.delete()


            return Response ({
            'respuesta': 'Mesa eliminada'
            }, status = status.HTTP_200_OK)

        except Mesas.DoesNotExist:

            return Response({
                'Errors': "La mesa no existe"
            }, status = status.HTTP_404_NOT_FOUND)

class EliminarVariasMesasVista(APIView):
  
  permission_classes = [IsAuthenticated, IsActiveUserPermission]

  def delete(self, request):
        
        serializer = EliminarVariasMesasSerializer(data=request.data)

        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        ids = serializer.validated_data.get('ids', [])


        if not ids:
            return Response({"Errors": "No se proporcionaron IDS para eliminar"}, status=status.HTTP_400_BAD_REQUEST)

        
        registros_eliminados = Mesas.objects.filter(id__in=ids).delete()

        
        if registros_eliminados[0] > 0:
            return Response({"respuesta":  "Mesas eliminadas correctamente"}, status=status.HTTP_200_OK)
        else:
            return Response({"Errors": "No se encontraron mesas para eliminar"}, status=status.HTTP_404_NOT_FOUND)

class CrearVentaVista(APIView):

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
        serializer = CrearVentaSerializer(data = request.data, context = {'usuario': usuario.nombre})
        
        
        if serializer.is_valid():
          
          serializer.save()

          return Response({
             "respuesta": "Nueva venta creada"
          }, status = status.HTTP_200_OK)

        else:
            
            return Response({
                "Errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
       
class VerVentasVista(APIView):

    permission_classes = [IsAuthenticated, IsActiveUserPermission]

    def get(self, request, *args, **kwargs):

        try:


            venta = Ventas.objects.all()

            paginator = PageNumberPagination()
            resultado_paginas = paginator.paginate_queryset(venta, request)    
            
            serializer = VerVentaSerializer(resultado_paginas, many = True)

            total_paginas = paginator.page.paginator.num_pages

            return paginator.get_paginated_response(
               {
                    'total_paginas': total_paginas,
                    'datos': serializer.data
                }
           )
        
        except Exception as e:

            return Response({
                'Errors': str(e)
            }, status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class VerVentaPorIdVista(APIView):

    permission_classes = [IsAuthenticated, IsActiveUserPermission]

    def get(self, request, *args, **kwargs):

        try:

            id_venta = kwargs['id']

            venta = Ventas.objects.get(id = id_venta)

            serializers = VerEditarVentaSerializer(venta)

            return Response({
                'respuesta': serializers.data
            })

        except Ventas.DoesNotExist:

            return Response({
                "Errors": "Venta no encontrada"
            }, status = status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"Errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ActualizarVentaPorIDVista(APIView):

    permission_classes = [IsAuthenticated, IsActiveUserPermission]

    def put(self, request, *args, **kwargs):

        access_token = request.headers.get('Authorization').split(' ')[-1] 

      
        if not access_token:
                
            return Response({
            'Errors': "No se ha proporcionado un token de acceso"
            })          
        
        
        token = AccessToken(access_token)
        usuario_id = token.payload['user_id']
        usuario = Usuarios.objeto.get(id = usuario_id)

        try:

            id = kwargs['id']
            venta = Ventas.objects.get(id = id)
        
        except Ventas.DoesNotExist:

            return Response({"Errors": "Venta no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ActualizarVentaSerializer(venta, data = request.data, context = {'usuario': usuario.nombre})

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class EliminarVentaPorIdVista(APIView):

    permission_classes = [IsAuthenticated, IsActiveUserPermission]

    def delete(self, data, *args, **kwargs):

        id = kwargs['id']

        try:

            venta = Ventas.objects.get(id = id)
            venta.delete()


            return Response ({
            'respuesta': 'Venta eliminada'
            }, status = status.HTTP_200_OK)

        except Ventas.DoesNotExist:

            return Response({
                'Errors': "La venta no existe"
            }, status = status.HTTP_404_NOT_FOUND)
        
class EliminarVariasVentasVista(APIView):
  
  permission_classes = [IsAuthenticated, IsActiveUserPermission]

  def delete(self, request):
        
    
        serializer = EliminarVariasVentasSerializer(data=request.data)

        

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        ids = serializer.validated_data.get('ids', [])


        if not ids:
            return Response({"Errors": "No se proporcionaron IDS para eliminar"}, status=status.HTTP_400_BAD_REQUEST)

        
        registros_eliminados = Ventas.objects.filter(id__in=ids).delete()

        
        if registros_eliminados[0] > 0:
            return Response({"respuesta":  "Ventas eliminadas correctamente"}, status=status.HTTP_200_OK)
        else:
            return Response({"Errors": "No se encontraron ventas para eliminar"}, status=status.HTTP_404_NOT_FOUND)
        
class BuscarVentaPorUnaFechaVista(APIView):

    permission_classes = [IsAuthenticated, IsActiveUserPermission]

    def get(self, request, *args, **kwargs):

        try:
            fecha_string = request.query_params.get('fecha', None)

            if fecha_string is None:
                return Response({"Errors": "Fecha no proporcionada."}, status=status.HTTP_400_BAD_REQUEST)

            fecha = datetime.strptime(fecha_string, '%Y-%m-%d').date()

            venta = Ventas.objects.filter(fecha_creacion__date=fecha)
    
            if venta.exists():


                paginator = PageNumberPagination()
                resultado_paginas = paginator.paginate_queryset(venta, request)    
                
                serializer = VerVentaSerializer(resultado_paginas, many = True)

                total_paginas = paginator.page.paginator.num_pages


                return paginator.get_paginated_response(
               {
                    'total_paginas': total_paginas,
                    'datos': serializer.data
                }
                )


            else:
                return Response({"Errors": "Venta no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"Errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class BuscarVentaRangoDosFechasVista(APIView):

    permission_classes = [IsAuthenticated, IsActiveUserPermission]

    def get(self, request, *args, **kwargs):

        try:

            fecha_inicial_string = kwargs['fecha_inicial']
            fecha_final_string = kwargs['fecha_final']

    

            if not fecha_inicial_string or not fecha_final_string:
                return Response({"Errors": "No se han proporcionado las dos fechas."}, status=status.HTTP_400_BAD_REQUEST)


            fecha_inicial = datetime.strptime(fecha_inicial_string, '%Y-%m-%d').date()
            fecha_final = datetime.strptime(fecha_final_string, '%Y-%m-%d').date()

            venta = Ventas.objects.filter(fecha_creacion__date__range = (fecha_inicial, fecha_final))
    
            if venta.exists():


                paginator = PageNumberPagination()
                resultado_paginas = paginator.paginate_queryset(venta, request)    
                
                serializer = VerVentaSerializer(resultado_paginas, many = True)

                total_paginas = paginator.page.paginator.num_pages


                return paginator.get_paginated_response(
               {
                    'total_paginas': total_paginas,
                    'datos': serializer.data
                }
                )


            else:
                return Response({"Errors": "Venta no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"Errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        