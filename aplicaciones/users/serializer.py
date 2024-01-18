from rest_framework import serializers
from .models import Usuarios

from .functions import *

class VerUsuarios(serializers.ModelSerializer):
   
  class Meta:
    
    model = Usuarios
    fields = (
      'id',
      'nombre',
      'cargo',
      'is_active',
      'fecha_creacion'
      
    )

class VerUsuarioPorIdSerializer(serializers.ModelSerializer):

  class Meta:
    
    model = Usuarios
    fields = (
      'id',
      'nombre',
      'cargo',
      'is_active',
      
    )

class LoginEmailPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UsuarioEmailPassword(serializers.ModelSerializer):
   
  repetir_password = serializers.CharField(write_only=True)

  class Meta:
      model = Usuarios
      fields = (
          'nombre',
          'email',
          'password',
          'repetir_password',
          'cargo',
      )
      

  def validate(self, data):
      password = data.get('password')
      repetir_password = data.get('repetir_password')

      if password != repetir_password:
          raise serializers.ValidationError("Las contraseñas no coinciden")

      caracteres = len(password)

      if not 8 <= caracteres <= 20:
          raise serializers.ValidationError("La contraseña debe tener entre 8 y 20 caracteres")

      return data

  def create(self, validated_data):
        
        repetir_password = validated_data.pop('repetir_password', None)

        # Asegúrate de incluir el campo repetir_password en el método de creación si es necesario
        # Puedes manipular los datos y llamar a tu método para crear el usuario aquí
        nuevo_usuario = Usuarios.objeto.crear_usuario_email_password(**validated_data)

        return nuevo_usuario
  
class UsuarioFacebookGmailSerializer(serializers.ModelSerializer):
   
   class Meta:
       
      model = Usuarios

      fields = (
          'nombre',
          'email',
          'cargo'
      )

   def create(self, validated_data):
      
      usario_nuevo = Usuarios.objeto.crear_usuario_gmail_facebook(**validated_data)

      return usario_nuevo
      
class LoginGmailFacebookSerializer(serializers.Serializer):


  email = serializers.EmailField()
  is_active = serializers.BooleanField(read_only=True)

  def validate(self, data):

    email = data.get('email')

  
    try:

      user = Usuarios.objeto.get(email = email)
    
      return user

    except Usuarios.DoesNotExist:

      raise serializers.ValidationError('El usuario no existe')

class UsuarioActualizarPorIdSerializer(serializers.ModelSerializer):

  class Meta:
    
    model = Usuarios
    fields = (
      'nombre',
      'cargo',
      'is_active',
      
    )

class EliminarVariosUsuariosSerializer(serializers.Serializer):

  ids = serializers.ListField(child=serializers.IntegerField())

class BuscarUsuarioNombreSerializer(serializers.Serializer):

  nombre = serializers.CharField()

class GenerarCodigoRecuperacionPasswordSerializer(serializers.Serializer):

  email = serializers.EmailField()


class RecuperarPasswordSerializer(serializers.Serializer):

  email = serializers.EmailField()
  password = serializers.CharField()
  codigo_recuperar_cuenta = serializers.CharField()