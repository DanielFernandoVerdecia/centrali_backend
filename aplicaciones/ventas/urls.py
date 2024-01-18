from django.urls import path

from .views import *

urlpatterns = [

    path('api/ver_mesas', VerMesasVista.as_view()),
    path('api/buscar_mesa', BuscarMesaPorNombreVista.as_view()),
    path('api/crear_mesa', CrearMesaVisa.as_view()),
    path('api/ver_mesa_por_id/<id>/', VerMesaPorIdVista.as_view()),
    path('api/editar_mesa/<id>/', EditarMesaVista.as_view()),
    path('api/eliminar_mesa_por_id/<id>/', EliminarMesaPorIdVista.as_view()),
    path('api/eliminar_varias_mesas', EliminarVariasMesasVista.as_view()),

    path('api/crear_venta', CrearVentaVista.as_view()),

    path('api/ver_ventas', VerVentasVista.as_view()),

    path('api/ver_venta_por_id/<id>/', VerVentaPorIdVista.as_view()),

    path('api/actualizar_venta_por_id/<id>/', ActualizarVentaPorIDVista.as_view()),

    path('api/eliminar_venta_por_id/<id>/', EliminarVentaPorIdVista.as_view()),

    path('api/eliminar_varias_ventas', EliminarVariasVentasVista.as_view()),

    path('api/buscar_venta_una_fecha', BuscarVentaPorUnaFechaVista.as_view()),

    path('api/buscar_venta_rango_fechas/<fecha_inicial>/<fecha_final>/', BuscarVentaRangoDosFechasVista.as_view())

]