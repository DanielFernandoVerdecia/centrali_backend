from django.contrib.auth.models import BaseUserManager
from django.db import models

from django.contrib.auth.hashers import make_password

class UsuarioManager(BaseUserManager, models.Manager):


    def _create_user(self, nombre, email, password, is_staff, is_superuser , is_active, cargo , **extra_fields):

        nuevo_usuario = self.model(

            nombre = nombre,
            email = email,
            is_staff = is_staff,
            is_superuser = is_superuser,
            is_active = is_active,
            cargo = cargo,
            **extra_fields

        )

        nuevo_usuario.password = make_password(password)

        nuevo_usuario.save(using = self.db)

        return nuevo_usuario

    def create_superuser(self, nombre, email, password, **extra_fields):

        return self._create_user(
            nombre = nombre,
            email = email, 
            password = password,
            is_staff = True,
            is_superuser = True,
            is_active = True,
            **extra_fields
        )
    
    def crear_usuario_email_password(self, nombre, email, password, cargo, **extra_fields):

        return self._create_user(
            nombre = nombre,
            email = email,
            password = password,
            is_staff = False,
            is_superuser = False,
            is_active = False,
            cargo = cargo,
            **extra_fields
        )


    def crear_usuario_gmail_facebook(self, nombre, email, cargo ,**extra_fields):

        return self._create_user(
            nombre = nombre,
            email = email,
            password = None,
            is_staff = False,
            is_superuser = False,
            is_active = False,
            cargo = cargo,
            **extra_fields

        )
        
    def verificar_codigo_activar_cuenta(self, id, codigo_ingresado):

        if self.filter(
            id = id, 
            codigo_activar_cuenta = codigo_ingresado
        ).exists():
            
            return True
        
    def verificar_codigo_recuperar_cuenta(self, id, codigo_ingresado):

        if self.filter(
            id = id, 
            codigo_recuperar_cuenta = codigo_ingresado
        ).exists():
            
            return True