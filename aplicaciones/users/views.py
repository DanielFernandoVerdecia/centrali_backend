
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Usuarios
from .serializer import *

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from ..permission_class import *
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token

from django.contrib.auth.hashers import check_password, make_password


from rest_framework.pagination import PageNumberPagination

from django.contrib.postgres.search import TrigramSimilarity

from rest_framework_simplejwt.tokens import AccessToken

from django.core.mail import send_mail

from .functions import *

"""
class VerTodosLosUsuarios(APIView):

    def get(self, request, format=None, *args, **kwargs):
            
        usarios = Usuarios.objeto.all()
        serializer = UsuarioSerializer(usarios, many=True)
        
        return Response(serializer.data)
"""

class VerTodosUsuarios(APIView):
   
   
   def get(self, request, *args, **kwargs):
        
        try:

            usuarios = Usuarios.objects.all()

            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(usuarios, request)
            
            serializers = VerUsuarios(result_page, many=True)

            total_paginas = paginator.page.paginator.num_pages
            
            return paginator.get_paginated_response({

                'total_paginas': total_paginas,
                'datos': serializers.data

            })

        except Exception as e:
            return Response({"Errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerUsuarioPorId(APIView):
   
   permission_classes = [IsAuthenticated, IsActiveUserPermission, IsJefeUserPermission]

   def get(self, request, *args, **kwargs):
        
        try:

            id_usuario = kwargs['id']

            usuario = Usuarios.objects.get(id = id_usuario)

            serializers = VerUsuarioPorIdSerializer(usuario)

            return Response({
                'respuesta': serializers.data
            })

        except Usuarios.DoesNotExist:

            return Response({
                "Errors": "Usuario no encontrado"
            }, status = status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"Errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UsuarioIdByTokenVista(APIView):

    permission_classes = [IsAuthenticated, IsActiveUserPermission, IsJefeUserPermission]

    def get(self, request, *args, **kwargs):

       access_token = request.headers.get('Authorization').split(' ')[-1] 

       if not access_token:
            
        return Response({
           'Errors': "No se ha proporcionado un token de acceso"
           
        })          
       
       try:

        token = AccessToken(access_token)
        usuario_id = token.payload['user_id']
        usuario = Usuarios.objeto.get(id = usuario_id)

        return Response({
                'respuesta': usuario.id
            })

       except Usuarios.DoesNotExist:

            return Response({
                "Errors": "Usuario no encontrado"
            }, status = status.HTTP_404_NOT_FOUND)

       except Exception as e:
         return Response({"Errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CrearUsuarioEmailPassword(APIView):

    def post(self, request, *args, **kwargs):

        serializer = UsuarioEmailPassword(data = request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        error_obtenido = {
            'Errors': serializer.errors
        } 

        return Response(error_obtenido, status=status.HTTP_400_BAD_REQUEST)

class CrearUsuarioFacebookGmail(APIView):


    def post(self, request, *args, **kwargs):

        serializer = UsuarioFacebookGmailSerializer(data = request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        error_obtenido = {
            'Errors': serializer.errors
        } 

        return Response(error_obtenido, status=status.HTTP_400_BAD_REQUEST)

class LoginEmailPasswordVista(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginEmailPasswordSerializer(data=request.data)

        if serializer.is_valid():
                
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']

                try:

                    usuario = Usuarios.objeto.get(email=email)

                except Usuarios.DoesNotExist:
                    return Response({'Errors': 'Usuario no existe.'}, status=status.HTTP_401_UNAUTHORIZED)

                if usuario.codigo_recuperar_cuenta and check_password(password , usuario.codigo_recuperar_cuenta):
                    return Response({'respuesta': True, 'codigo_verificacion': usuario.codigo_recuperar_cuenta})

                elif usuario.codigo_recuperar_cuenta and check_password(password , usuario.codigo_recuperar_cuenta) == False:

                    return Response({'Errors': 'El código de recuperación de contraseña es inválido.'}, status=status.HTTP_401_UNAUTHORIZED)

                else:

                
                    if check_password(password, usuario.password) and usuario.is_active:
                        refresh = RefreshToken.for_user(usuario)
                        return Response({
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            'nombre': usuario.nombre,
                            'cargo': usuario.cargo
                        })

                    elif check_password(password, usuario.password) == False:

                        return Response({'Errors': 'Email o contraseña incorrecto.'}, status=status.HTTP_401_UNAUTHORIZED)
                    
                    else:

                        return Response({'Errors': 'Cuenta no verificada, debe esperar a que un Jefe active su cuenta.'}, status=status.HTTP_401_UNAUTHORIZED)



        else:
            return Response({'Errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginFacebookGmail(APIView):

   def post(self, request, *args, **kwargs):
        
        serializer = LoginGmailFacebookSerializer(data=request.data)

        try:

            serializer.is_valid(raise_exception=True)

        except serializers.ValidationError as error:
            return Response({'Errors': error.detail}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data

        is_active = user.is_active

        if is_active:

            refresh = RefreshToken.for_user(user)

            return Response({

                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'nombre': user.nombre,
                'cargo': user.cargo
            })
        
        return Response({'Errors': 'Cuenta no verificada, debe esperar a que un Jefe active su cuenta.'}, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutUsuario(APIView):

    def post(self, request):

        try:

            refresh_token = request.headers.get('Authorization')

            token = RefreshToken(refresh_token)
            
            token.blacklist()

            return Response({"Detalle": "Logout exitoso."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"Detalle": "Error al hacer logout."}, status=status.HTTP_400_BAD_REQUEST)

class ValidarTokenUserIsActiveVista(APIView):

    def get(self, request, *args, **kwargs):

        access_token = request.headers.get('Authorization').split(' ')[-1] 

        if not access_token:
                
            return Response({
            'Respuesta': False
            
            })          
        
        
        token = AccessToken(access_token)
        usuario_id = token.payload['user_id']
        usuario = Usuarios.objeto.get(id = usuario_id)

        if usuario.is_active:

            return Response({
            'Respuesta': True
            }) 
        
        else:

            return Response({
            'Respuesta': False
            }) 

class ValidarTokenUserIsJefeVista(APIView):

    def get(self, request, *args, **kwargs):

        access_token = request.headers.get('Authorization').split(' ')[-1] 

        if not access_token:
                
            return Response({
            'Respuesta': False
            
            })          
        
        
        token = AccessToken(access_token)
        usuario_id = token.payload['user_id']
        usuario = Usuarios.objeto.get(id = usuario_id)

        if usuario.cargo == 'Jefe':

            return Response({
            'Respuesta': True
            }) 
        
        else:

            return Response({
            'Respuesta': False
            })
                      
class ActualizarUsuarioPorID(APIView):

    permission_classes = [IsAuthenticated, IsActiveUserPermission, IsJefeUserPermission]

    def put(self, request, *args, **kwargs):

        try:

            id = kwargs['id']
            usuario_obtenido = Usuarios.objeto.get(id = id)
        
        except Usuarios.DoesNotExist:

            return Response({"Errors": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UsuarioActualizarPorIdSerializer(usuario_obtenido, data = request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class EliminarUsuarioPorId(APIView):

    permission_classes = [IsAuthenticated, IsActiveUserPermission, IsJefeUserPermission]

    def delete(self, data, *args, **kwargs):

        id = kwargs['id']

        try:

            usuario = Usuarios.objeto.get(id = id)
            usuario.delete()

            return Response ({
            'respuesta': 'Usuario eliminado'
            }, status = status.HTTP_200_OK)

        except Usuarios.DoesNotExist:

            return Response({
                'Errors': "El usuario no existe"
            }, status = status.HTTP_404_NOT_FOUND)
        
class EliminarVariosUsuariosPorId(APIView):
  
  permission_classes = [IsAuthenticated, IsActiveUserPermission, IsJefeUserPermission]

  def delete(self, request):
        
        serializer = EliminarVariosUsuariosSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        ids = serializer.validated_data.get('ids', [])

        if not ids:
            return Response({"Errors": "No se proporcionaron IDS para eliminar"}, status=status.HTTP_400_BAD_REQUEST)

        
        registros_eliminados = Usuarios.objeto.filter(id__in=ids).delete()

        
        if registros_eliminados[0] > 0:
            return Response({"respuesta":  "registros eliminados correctamente"}, status=status.HTTP_200_OK)
        else:
            return Response({"Errors": "No se encontraron registros para eliminar"}, status=status.HTTP_404_NOT_FOUND)

class BuscarUsuariosPorNombre(APIView):
  
  permission_classes = [IsAuthenticated, IsActiveUserPermission, IsJefeUserPermission]

  def get(self, request):
        
        
        nombre = request.query_params.get('nombre', '')

        if not nombre:
            
            return Response({"Errors": "No se proporcionó el nombre"}, status=status.HTTP_400_BAD_REQUEST)

        try:

            usuarios_encontrados = Usuarios.objeto.filter(
                nombre__trigram_similar=nombre
            )

            
            if not usuarios_encontrados.exists():
                return Response({"Errors": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)



            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(usuarios_encontrados, request)
            
            serializers = VerUsuarios(result_page, many=True)

            total_paginas = paginator.page.paginator.num_pages
            
            return paginator.get_paginated_response({

                'total_paginas': total_paginas,
                'datos': serializers.data

            })    
      
          

        except Exception as e:
            return Response({"Errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GenerarCodigoRecuperacionPasswordVista(APIView):

    def put(self, request, *args, **kwargs):

        serializer = GenerarCodigoRecuperacionPasswordSerializer(data = request.data)

        if serializer.is_valid():

            try:
                usuario = Usuarios.objects.get(email=serializer.data['email'])

                codigo_recuperacion = generar_codigo_cuenta()
            
                usuario.codigo_recuperar_cuenta = make_password(codigo_recuperacion)

                usuario.save()

                asunto = "Código de recuperacion de cuenta Centrali"
                mensaje = "Su código de recuperación de cuenta es: " + codigo_recuperacion + " , recuerde que debe ingresarlo junto a su cuenta en el login para después crear una nueva contraseña."
                email_remitente = "centralioficial@gmail.com"
                email_destinatario = usuario.email

                try:
                    send_mail(
                        asunto,
                        mensaje,
                        email_remitente,
                        [email_destinatario, ]
                )  
                    return Response({
                        'respuesta': 'Ok'
                    }) 
                    
                except Exception as e:
                    return Response({'Errors': "Error al enviar código de recuperación"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

            except Usuarios.DoesNotExist:
                return Response({'Errors': "No se encontró ningún usuario con este correo electrónico."}, status=status.HTTP_404_NOT_FOUND)


        error_obtenido = {
            'Errors': serializer.errors
        } 

        return Response(error_obtenido, status=status.HTTP_400_BAD_REQUEST)




    def get(self, request, *args, **kwargs):

        serializer = GenerarCodigoRecuperacionPasswordSerializer(data = request.data)

        if serializer.is_valid():

            try:
                usuario = Usuarios.objects.get(email=serializer.data['email'])

                codigo_recuperacion = generar_codigo_cuenta()
            
                usuario.codigo_recuperar_cuenta = codigo_recuperacion

                usuario.save()

                asunto = "Código de recuperacion de cuenta Centrali"
                mensaje = "Su código de recuperación de cuenta es: " + codigo_recuperacion + " , recuerde que debe ingresarlo junto a su cuenta en el login para después crear una nueva contraseña."
                email_remitente = "centralioficial@gmail.com"
                email_destinatario = usuario.email

                try:
                    send_mail(
                        asunto,
                        mensaje,
                        email_remitente,
                        [email_destinatario, ]
                )  
                    return Response({
                        'respuesta': 'Ok'
                    }) 
                    
                except Exception as e:
                    return Response({'Errors': "Error al enviar el correo"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

            except Usuarios.DoesNotExist:
                return Response({'Errors': "No existe el usuario."}, status=status.HTTP_404_NOT_FOUND)


        error_obtenido = {
            'Errors': serializer.errors
        } 

        return Response(error_obtenido, status=status.HTTP_400_BAD_REQUEST)

class CambiarPasswordUserEmailPasswordVista(APIView):

    def put(self, request, *args, **kwargs):

        serializer = RecuperarPasswordSerializer(data = request.data)

        if serializer.is_valid():

            try:

                usuario = Usuarios.objeto.get(
                    email = serializer.validated_data['email'],
                    codigo_recuperar_cuenta = serializer.validated_data['codigo_recuperar_cuenta'] 
                ) 

                

                usuario.set_password(serializer.validated_data['password'])
                usuario.codigo_recuperar_cuenta = None

                usuario.save()

                return Response({
                    'Respuesta': 'Ok'
                })

            except Usuarios.DoesNotExist:

                return Response({'Errors': 'No se puede cambiar la contraseña'}, status = status.HTTP_404_NOT_FOUND)

        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
