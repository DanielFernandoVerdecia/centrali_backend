from django.urls import path

from .views import *

urlpatterns = [

    path('api/ver_todos_los_usuarios', VerTodosUsuarios().as_view()),
    path('api/ver_usuario/<id>/', VerUsuarioPorId().as_view()),
    path('api/usuario_id_by_token_vista', UsuarioIdByTokenVista().as_view()),
    path('api/crear_usuario_email_password', CrearUsuarioEmailPassword().as_view()),
    path('api/crear_usuario_facebook_gmail', CrearUsuarioFacebookGmail().as_view()),
    path('api/actualizar_usuario/<id>/', ActualizarUsuarioPorID().as_view()),
    path('api/eliminar_usuario/<id>/', EliminarUsuarioPorId().as_view()),
    path('api/eliminar_varios_usuarios', EliminarVariosUsuariosPorId().as_view()),
    path('api/validar_token_usuario_is_active', ValidarTokenUserIsActiveVista().as_view()),
    path('api/validar_token_user_is_jefe_vista', ValidarTokenUserIsJefeVista().as_view()),
    path('api/buscar_usuario_por_nombre', BuscarUsuariosPorNombre().as_view()),
    path('api/login_usuario_facebook_gmail', LoginFacebookGmail().as_view()),
    path('api/login_email_password_vista', LoginEmailPasswordVista().as_view()),
    path('api/logout_usuario', LogoutUsuario().as_view()),
    path('api/generar_codigo_recuperacion_password_vista', GenerarCodigoRecuperacionPasswordVista().as_view()),
    path('api/cambiar_password_user_email_passwor_vista', CambiarPasswordUserEmailPasswordVista().as_view()),
    
    
]

