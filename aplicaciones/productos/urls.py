from django.urls import path

from .views import *

urlpatterns = [

    path('api/crear_producto', CrearProductoVista().as_view()),
    path('api/ver_productos', VerProductosVista().as_view()),
    path('api/id_productos_vista', IdProductosVista().as_view()),
    path('api/ver_producto_por_id/<id>/', VerProductoPorIdVista().as_view()),
    path('api/actualizar_producto_por_id/<id>/', ActualizarProductoPorIDVista().as_view()),
    path('api/eliminar_producto_por_id/<id>/', EliminarProductoPorIdVista().as_view()),
    path('api/eliminar_varios_productos', EliminarVariosProductosVista().as_view()),
    path('api/buscar_producto_por_nombre', BuscarProductosPorNombreVista().as_view()),
]