from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('aplicaciones.users.urls')),
    path('', include('aplicaciones.productos.urls')),
    path('', include('aplicaciones.ventas.urls')),
]
