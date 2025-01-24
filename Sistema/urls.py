"""
URL configuration for Sistema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from Datos import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path


urlpatterns = [
    #forms
    path('home2/', views.home2, name = 'home2'),
    path('registro_espacio/', views.registro_espacio, name='registro_parcela'),
    path('registro_planta/', views.registro_planta, name='registro_planta'),
    path('tipo_planta/', views.tipo_planta, name='tipo_planta'),
    
    #vistas
    path('vista_sensores/', views.vista_sensores, name='vista_sensores'),
    path('vista_espacios/', views.vista_espacios, name='vista_espacios'),
    path('detalle_espacio/<int:id_espacio>/', views.detalle_espacio, name='detalle_espacio'),
    path('editar_espacio/<int:id_espacio>/', views.editar_espacio, name='editar_espacio'),
    path('eliminar_espacio/<int:id_espacio>/', views.eliminar_espacio, name='eliminar_espacio'),

    path('modal/', views.modal_view, name='modal_view'),
    
    #otros
    path('admin/', admin.site.urls),
    path('obtener_temperatura/', views.datos_recientes, name='datos_recientes'),
    path('', views.home, name = 'home'),
    path('guardar_datos_sensor/', views.guardar_datos_sensor, name='guardar_datos_sensor'),
    path('detalle_dato/', views.detalle_dato, name='detalle_dato'),
    path('datos_recientes/', views.datos_recientes, name='datos_recientes'),
    path('mapa/', views.mapa, name='mapa'),

    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
